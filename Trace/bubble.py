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
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from recall import _content_words
from store import Decision, add_decision, connect, get_all_decisions, init_db

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
    "You are Trace, an ambient design-decision memory agent watching a construction "
    "project. Answer conversationally, grounded ONLY in the PROJECT CONTEXT and the "
    "DECISION RECORD provided.\n"
    "- Interpret questions charitably: tolerate typos and shorthand, and use the "
    "conversation history to resolve follow-ups like 'that clause' or 'who decided it'.\n"
    "- Cite decision ids inline like (D-001) whenever you state something from the record.\n"
    "- If asked about a design decision that is NOT in the record, reply exactly: "
    '"No decision on record; not yet decided."\n'
    "- If asked for a source document the record only cites (e.g. the full text of a "
    "fire-code clause), say what the record cites and that Trace stores the project's "
    "decision record, not the source documents — do NOT recite statutory text from memory.\n"
    "- If asked what Trace is or how to use this panel, answer from PROJECT CONTEXT.\n"
    "- Be concise: one to three sentences."
)

_HISTORY_LIMIT = 10  # messages kept as conversation memory (this is a memory agent, after all)
HOST = os.getenv("TRACE_HOST", "127.0.0.1")
PORT = int(os.getenv("TRACE_PORT", "8765"))


def _seed(conn) -> None:
    add_decision(conn, Decision(
        statement="Facade cladding = non-combustible mineral rainscreen (A1 core, Class 0)",
        discipline="facade", status="valid",
        rationale="Building is 95 m (> 15 m); SCDF Fire Code 2023 Cl 3.5 requires the facade "
                  "cladding to be wholly non-combustible above that height.",
        author=["K. Lim (QP)", "M. Ong (fire)"],
        recorded_at="2026-01-14T11:42Z", valid_from="2026-01-14T11:42Z",
    ))
    add_decision(conn, Decision(
        statement="Swap facade cladding to polyethylene-core ACP (combustible)",
        discipline="facade", status="proposed",
        rationale="VE cost saving under the 'or equivalent' clause — rejected: breaches Cl 3.5.",
        recorded_at="2026-03-03T14:00Z", valid_from="2026-03-03T14:00Z",
    ))


class Api:
    """The bubble's engine bridge — used by the web handler (and any native shell)."""

    def __init__(self):
        self.conn = connect(":memory:")
        init_db(self.conn)
        _seed(self.conn)
        self.history: list[dict] = []  # shared conversation memory for this server

    def state(self) -> str:
        decisions = [
            {"id": d.id, "status": d.status, "statement": d.statement}
            for d in get_all_decisions(self.conn)
        ]
        return json.dumps({"context": "Level 0 · facade", "decisions": decisions})

    def _record(self) -> str:
        lines = []
        for d in get_all_decisions(self.conn):
            lines.append(f"{d.id} [{d.status}] {d.statement}")
            if d.rationale:
                lines.append(f"   rationale: {d.rationale}")
            if d.assumptions:
                lines.append(f"   assumptions: {'; '.join(d.assumptions)}")
            if d.author:
                lines.append(f"   by: {', '.join(d.author)}  ·  valid from {(d.valid_from or '')[:10]}")
        return "\n".join(lines)

    def ask(self, question: str) -> str:
        try:
            import os

            import openai
            from recall import BASE_URL, MODEL
            client = openai.OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)
            messages = [
                {"role": "system", "content": _ASSISTANT_SYS},
                {"role": "system", "content":
                    f"PROJECT CONTEXT:\n{_PROJECT_BLURB}\n\nDECISION RECORD:\n{self._record()}"},
                *self.history[-_HISTORY_LIMIT:],
                {"role": "user", "content": question},
            ]
            resp = client.chat.completions.create(model=MODEL, temperature=0, messages=messages)
            answer = resp.choices[0].message.content.strip()
            self.history.extend([{"role": "user", "content": question},
                                 {"role": "assistant", "content": answer}])
            self.history = self.history[-_HISTORY_LIMIT:]
            known = {d.id for d in get_all_decisions(self.conn)}
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


_api = None


def _get_api() -> Api:
    global _api
    if _api is None:
        _api = Api()
    return _api


class _Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        raw = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._send(200, _HTML.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        elif path == "/state":
            self._send(200, _get_api().state())
        else:
            self._send(404, "{}")

    def do_POST(self):
        if self.path == "/ask":
            n = int(self.headers.get("Content-Length", 0) or 0)
            data = json.loads(self.rfile.read(n) or b"{}")
            self._send(200, _get_api().ask(data.get("question", "")))
        else:
            self._send(404, "{}")

    def log_message(self, *_):  # keep the console quiet
        pass


def main(open_browser: bool = True) -> None:
    server = HTTPServer((HOST, PORT), _Handler)
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
