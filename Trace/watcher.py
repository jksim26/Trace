"""The ambient desktop watcher (Windows) — the real-world half of the trigger.

Polls the FOREGROUND WINDOW TITLE once a second (title bar text only — no
screen capture, no OCR, no hooks) and, when a title matches the allowlist in
watch_rules.yaml, POSTs the document-open event to the local Trace bubble,
which pops the nudge. The browser workspace (/workspace) sends the identical
event through the identical matcher — one brain, two worlds.

Privacy by construction: only allowlisted patterns match; everything else is
ignored; the event goes to 127.0.0.1 only.

Run (Windows, with the bubble running):  python watcher.py
Options:  --url http://127.0.0.1:8765   --once "SOME TITLE"  (test the matcher)
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

from ambient import match_title

DEFAULT_URL = "http://127.0.0.1:8765"


def foreground_title() -> str:
    """Windows-only seam: read the foreground window's title bar text."""
    import ctypes
    u32 = ctypes.windll.user32
    hwnd = u32.GetForegroundWindow()
    n = u32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(n + 1)
    u32.GetWindowTextW(hwnd, buf, n + 1)
    return buf.value


def post_nudge(title: str, url: str) -> bool:
    req = urllib.request.Request(
        f"{url}/nudge", data=json.dumps({"title": title}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read()).get("matched", False)


def main() -> None:
    url = DEFAULT_URL
    if "--url" in sys.argv:
        url = sys.argv[sys.argv.index("--url") + 1]
    if "--once" in sys.argv:
        title = sys.argv[sys.argv.index("--once") + 1]
        m = match_title(title)
        print(f"match: {m}")
        if m:
            print("posted, matched:", post_nudge(title, url))
        return
    if sys.platform != "win32":
        sys.exit("watcher.py watches the Windows foreground window; on other "
                 "systems use the simulated workspace at /workspace instead.")
    print(f"Trace watcher — allowlist-only, local-only -> {url}  (Ctrl+C to stop)")
    last = ""
    while True:
        try:
            title = foreground_title()
            if title and title != last:
                last = title
                if match_title(title):
                    ok = post_nudge(title, url)
                    print(f"  ⛯ {title[:70]}  -> nudge {'sent' if ok else 'ignored'}")
        except Exception as exc:  # keep watching through transient errors
            print(f"  (watcher hiccup: {exc})")
        time.sleep(1)


if __name__ == "__main__":
    main()
