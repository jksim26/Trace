"""Trace ambient bubble — the bubble UI wired LIVE to the Trace engine.

v1 runs as a tiny local web app (Python stdlib http.server, no extra installs):
it serves bubble.html and answers /state and /ask from the real engine, so you
can open it in a browser and see it WORK (the chat is a real recall_decisions
call). The always-on-top *floating desktop window* is a thin native shell
(pywebview / Qt) we add once it can be tested visually.

Run:  python bubble.py   → serves http://127.0.0.1:8765 and opens your browser.
"""
from __future__ import annotations

import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from recall import recall_decisions
from store import Decision, add_decision, connect, get_all_decisions, init_db

_HTML = Path(__file__).with_name("bubble.html")
PORT = 8765


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

    def state(self) -> str:
        decisions = [
            {"id": d.id, "status": d.status, "statement": d.statement}
            for d in get_all_decisions(self.conn)
        ]
        return json.dumps({"context": "Level 0 · facade", "decisions": decisions})

    def ask(self, question: str) -> str:
        try:
            r = recall_decisions(self.conn, question, budget=600)
            return json.dumps({"answer": r.answer, "cited": r.cited})
        except Exception as exc:  # keep the UI alive on any hiccup
            return json.dumps({"answer": f"(couldn't reach Trace: {exc})", "cited": []})


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
    server = HTTPServer(("127.0.0.1", PORT), _Handler)
    url = f"http://127.0.0.1:{PORT}"
    print(f"Trace bubble  ->  {url}   (Ctrl+C to stop)")
    if open_browser:
        threading.Timer(0.6, lambda: _safe_open(url)).start()
    server.serve_forever()


def _safe_open(url):
    try:
        webbrowser.open(url)
    except Exception:
        pass


if __name__ == "__main__":
    main()
