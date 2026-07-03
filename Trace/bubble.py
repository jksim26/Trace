"""Trace ambient bubble — the bubble UI wired LIVE to the Trace engine.

v1 runs as a tiny local web app (Python stdlib http.server, no extra installs):
it serves bubble.html and answers /state and /ask from the real engine, so you
can open it in a browser and see it WORK (the chat is a real recall_decisions
call). The always-on-top *floating desktop window* is a thin native shell
(pywebview / Qt) we add once it can be tested visually.

Run:  python bubble.py   → serves http://127.0.0.1:8765 and opens your browser.
Deploy (e.g. Alibaba Cloud ECS — see deploy/README.md):
      TRACE_HOST=0.0.0.0 python bubble.py --no-browser
"""
from __future__ import annotations

import json
import os
import re
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional

from ambient import match_title
from court import get_court_records
from recall import _content_words
from scenarios import PROJECTS, build_store
from store import get_all_decisions

_DRAWINGS = Path(__file__).resolve().parent.parent / "demo" / "drawings"
_WORKSPACE = Path(__file__).with_name("workspace.html")

_HTML = Path(__file__).with_name("bubble.html")

# Small-talk words that shouldn't hit the decision store at all — a first-time
# visitor's "hi" deserves a pointer, not "No decision on record".
_SMALL_TALK = {"hello", "hey", "yo", "sup", "help", "test", "testing", "thanks", "thank", "you"}


def _is_greeting(question: str) -> bool:
    words = _content_words(question)
    return not words or words <= _SMALL_TALK


_PROJECT_BLURB = (
    "Trace is an ambient design-decision memory agent for AEC (construction) projects. "
    "This demo watches 'Tanglin Rise', a fictional 28-storey, 95 m residential tower in "
    "Singapore. Trace captures each design decision with its rationale and assumptions, "
    "fires an alert the moment a new proposal breaks an earlier decision's premise "
    "(a deterministic SCDF fire-code rule-pack plus an LLM premise check), convenes a "
    "three-role decision court whose verdicts are recorded, can rewind the record to any "
    "date (bi-temporal), and answers questions only from the recorded decisions — "
    "abstaining honestly when nothing is on record."
)

# One brain, full context: the LLM sees the project blurb, the ENTIRE decision
# record (packed within budget — trivial at demo scale), and the conversation so
# far, then decides for itself how to answer. Grounding is preserved by what it
# is given, not by keyword pre-routing: it is instructed to answer only from the
# record, cite decision ids, and abstain on unrecorded decisions.
_ASSISTANT_SYS = (
    "You are Trace, an ambient design-decision memory agent watching a PORTFOLIO of "
    "construction projects. Answer conversationally, grounded ONLY in the PROJECT "
    "RECORDS provided.\n"
    "- The records span multiple projects. The user is viewing one of them (stated "
    "below); default ambiguous questions to it — but if they name or clearly mean "
    "another project (typos and approximate names included), answer about THAT project "
    "and say which project you are answering about.\n"
    "- Interpret questions charitably: tolerate typos and shorthand, and use the "
    "conversation history to resolve follow-ups like 'that clause' or 'who decided it'.\n"
    "- Cite decision ids inline like (D-001) whenever you state something from a record "
    "(ids repeat across projects — the project name disambiguates).\n"
    "- If asked about a design decision that is NOT in any record, reply exactly: "
    '"No decision on record; not yet decided."\n'
    "- If asked for a source document the records only cite (e.g. the full text of a "
    "fire-code clause), say what the record cites and that Trace stores decision "
    "records, not the source documents — do NOT recite statutory text from memory.\n"
    "- If asked what Trace is or how to use this panel, answer from the TRACE CONTEXT.\n"
    "- Be concise: one to three sentences."
)

_HISTORY_LIMIT = 10  # messages kept as conversation memory (this is a memory agent, after all)
_HISTORY: list[dict] = []  # ONE conversation with Trace — it survives project switches
HOST = os.getenv("TRACE_HOST", "127.0.0.1")
PORT = int(os.getenv("TRACE_PORT", "8765"))


DEFAULT_PROJECT = "tanglin-rise"


_STORES: dict = {}


def _store_for(project: str):
    if project not in _STORES:
        _STORES[project] = build_store(project)
    return _STORES[project]


class Api:
    """The bubble's engine bridge. The `project` is the VIEWED default context —
    the assistant's memory spans all projects (it is one agent, one memory)."""

    def __init__(self, project: str = DEFAULT_PROJECT):
        self.project = project
        self.conn = _store_for(project)

    def state(self) -> str:
        decisions = [
            {"id": d.id, "status": d.status, "statement": d.statement}
            for d in get_all_decisions(self.conn)
        ]
        return json.dumps({
            "context": PROJECTS[self.project]["title"],
            "project": self.project,
            "projects": [{"key": k, "title": v["title"]} for k, v in PROJECTS.items()],
            "decisions": decisions,
        })

    def _record(self, conn) -> str:
        lines = []
        for d in get_all_decisions(conn):
            span = f"valid from {(d.valid_from or '')[:10]}"
            if d.valid_to:
                span += f" to {d.valid_to[:10]} (superseded by {d.superseded_by})"
            lines.append(f"{d.id} [{d.status}] {d.statement}")
            if d.rationale:
                lines.append(f"   rationale: {d.rationale}")
            if d.assumptions:
                lines.append(f"   assumptions: {'; '.join(d.assumptions)}")
            if d.author:
                lines.append(f"   by: {', '.join(d.author)}  ·  {span}")
        for r in get_court_records(conn):
            lines.append(
                f"COURT RECORD: proposal {r['proposal_id']} — {r['verdict']} "
                f"(breaks {r['breaks_id']}; {r['citation']}). "
                f"For: {r['for_argument']} Against: {r['against_argument']} "
                f"Ruling: {r['rationale']}"
            )
        return "\n".join(lines)

    def _all_records(self) -> str:
        parts = []
        for key, meta in PROJECTS.items():
            parts.append(
                f"=== PROJECT: {meta['title']}  [{key}] ===\n"
                f"{meta['blurb']}\n{self._record(_store_for(key))}"
            )
        return "\n\n".join(parts)

    def ask(self, question: str) -> str:
        try:
            import os

            import openai
            from recall import BASE_URL, MODEL
            client = openai.OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)
            messages = [
                {"role": "system", "content": _ASSISTANT_SYS},
                {"role": "system", "content":
                    f"TRACE CONTEXT:\n{_PROJECT_BLURB}\n\n"
                    f"The user is currently viewing: {PROJECTS[self.project]['title']} "
                    f"[{self.project}] — default ambiguous questions to it.\n\n"
                    f"PROJECT RECORDS:\n{self._all_records()}"},
                *_HISTORY[-_HISTORY_LIMIT:],
                {"role": "user", "content": question},
            ]
            resp = client.chat.completions.create(model=MODEL, temperature=0, messages=messages)
            answer = resp.choices[0].message.content.strip()
            _HISTORY.extend([{"role": "user", "content": question},
                             {"role": "assistant", "content": answer}])
            del _HISTORY[:-_HISTORY_LIMIT]
            known = {d.id for k in PROJECTS for d in get_all_decisions(_store_for(k))}
            cited, seen = [], set()
            for did in re.findall(r"D-\d{3}", answer):
                if did in known and did not in seen:
                    seen.add(did)
                    cited.append(did)
            return json.dumps({"answer": answer, "cited": cited})
        except Exception:
            # No key / no network: degrade to the deterministic layer — a pointer
            # for greetings, the honest abstention otherwise. Never crash the UI.
            if _is_greeting(question):
                return json.dumps({
                    "answer": 'Hi! I answer from this project\'s decision record. Try: '
                              '"why the non-combustible facade cladding?" or '
                              '"can we still change the facade?"',
                    "cited": [],
                })
            return json.dumps({"answer": "No decision on record; not yet decided.", "cited": []})


# Latest ambient nudge — written by /nudge (watcher or workspace), polled by
# the bubble UI. Everything in it is built LIVE from the store at match time.
_NUDGE: dict = {"seq": 0}


def build_nudge(title: str) -> Optional[dict]:
    """Run the shared matcher over a window/document title; on a hit, build the
    nudge from the REAL store: relevant decisions ranked by keyword overlap,
    with live statuses. Returns None when the title matches no allowlist rule."""
    m = match_title(title)
    if m is None:
        return None
    api = _get_api(m.project)
    kw = _content_words(m.keywords)
    ranked = sorted(
        get_all_decisions(api.conn),
        key=lambda d: -len(kw & _content_words(
            f"{d.statement} {d.rationale} {' '.join(d.assumptions)}")),
    )
    rows = [{"id": d.id, "status": d.status, "statement": d.statement}
            for d in ranked[:4]]
    global _NUDGE
    _NUDGE = {
        "seq": _NUDGE["seq"] + 1,
        "project": m.project,
        "context": f"{PROJECTS[m.project]['title'].split('·')[0].strip()} — {m.context}",
        "decisions": rows,
        "title": title,
    }
    return _NUDGE


_apis: dict[str, Api] = {}


def _get_api(project: str = DEFAULT_PROJECT) -> Api:
    if project not in PROJECTS:
        project = DEFAULT_PROJECT
    if project not in _apis:
        _apis[project] = Api(project)
    return _apis[project]


def _query_param(path: str, name: str) -> str:
    from urllib.parse import parse_qs, urlparse
    return (parse_qs(urlparse(path).query).get(name) or [""])[0]


class _Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        raw = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_bytes(self, code, raw: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._send(200, _HTML.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        elif path == "/workspace":
            self._send(200, _WORKSPACE.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        elif path == "/state":
            self._send(200, _get_api(_query_param(self.path, "project")).state())
        elif path == "/nudge-state":
            self._send(200, json.dumps(_NUDGE))
        elif path.startswith("/drawings/"):
            name = Path(path).name  # no traversal: basename only
            f = _DRAWINGS / name
            if f.is_file():
                self._send_bytes(200, f.read_bytes(), "application/pdf")
            else:
                self._send(404, "{}")
        else:
            self._send(404, "{}")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        data = json.loads(self.rfile.read(n) or b"{}")
        if self.path == "/ask":
            api = _get_api(data.get("project") or DEFAULT_PROJECT)
            self._send(200, api.ask(data.get("question", "")))
        elif self.path == "/nudge":
            nudge = build_nudge(data.get("title", ""))
            self._send(200, json.dumps({"matched": nudge is not None,
                                        **({"seq": nudge["seq"]} if nudge else {})}))
        else:
            self._send(404, "{}")

    def log_message(self, *_):  # keep the console quiet
        pass


def main(open_browser: bool = True) -> None:
    # Threading: a browser PDF viewer can hold its connection open; a
    # single-threaded server would queue the nudge polls behind it forever.
    server = ThreadingHTTPServer((HOST, PORT), _Handler)
    url = f"http://{HOST}:{PORT}"
    print(f"Trace bubble  ->  {url}   (Ctrl+C to stop)")
    if open_browser and HOST == "127.0.0.1":
        threading.Timer(0.6, lambda: _safe_open(url)).start()
    server.serve_forever()


def _safe_open(url):
    try:
        webbrowser.open(url)
    except Exception:
        pass


if __name__ == "__main__":
    main(open_browser="--no-browser" not in sys.argv)
