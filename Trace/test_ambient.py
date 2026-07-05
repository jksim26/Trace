"""The ambient trigger: one matcher, two worlds. These tests prove the brain
is shared and the nudge is built LIVE from the store — never canned."""
import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import bubble
from ambient import match_title
from watcher import post_nudge


def test_real_window_titles_match():
    # Exactly what Acrobat / Edge / Revit put in the title bar.
    m = match_title("Tanglin-Rise_L01_Fire-Plan.pdf - Adobe Acrobat")
    assert m and m.project == "tanglin-rise" and "fire plan" in m.context
    m = match_title("Tanglin Rise - Floor Plan: Level 1 - Autodesk Revit 2026")
    assert m and m.project == "tanglin-rise"
    m = match_title("Maple-Wharf_East-Elevation.pdf - Microsoft Edge")
    assert m and m.project == "maple-wharf"


def test_allowlist_ignores_everything_else():
    for title in ["WhatsApp", "Inbox - Outlook", "invoice_2026.pdf - Adobe Acrobat",
                  "Tanglin Rise holiday photos.jpg", ""]:
        assert match_title(title) is None, title


def test_nudge_is_built_live_from_the_store():
    nudge = bubble.build_nudge("Tanglin-Rise_L01_Fire-Plan.pdf - Adobe Acrobat")
    assert nudge is not None
    ids = [d["id"] for d in nudge["decisions"]]
    assert "D-001" in ids                       # the live facade constraint
    statuses = {d["id"]: d["status"] for d in nudge["decisions"]}
    assert statuses["D-001"] == "valid"         # statuses come from SQLite, not strings
    assert nudge["project"] == "tanglin-rise"
    # A different drawing -> a different project's memory. Same brain, live data.
    nudge2 = bubble.build_nudge("Kranji-Hub_GF_Switchboard-Layout.pdf")
    assert nudge2["project"] == "kranji-hub"
    assert nudge2["seq"] == nudge["seq"] + 1
    assert any("switchboard" in d["statement"].lower() for d in nudge2["decisions"])


def test_unmatched_title_builds_no_nudge():
    seq_before = bubble._NUDGE["seq"]
    assert bubble.build_nudge("Inbox - Outlook") is None
    assert bubble._NUDGE["seq"] == seq_before


def test_http_round_trip_watcher_to_nudge_state():
    # The exact wire path watcher.py and the workspace both use.
    server = ThreadingHTTPServer(("127.0.0.1", 0), bubble._Handler)
    port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        url = f"http://127.0.0.1:{port}"
        assert post_nudge("Tanglin-Rise_L20_Sky-Terrace.pdf - Adobe Acrobat", url) is True
        with urllib.request.urlopen(f"{url}/nudge-state", timeout=5) as r:
            state = json.loads(r.read())
        assert state["project"] == "tanglin-rise" and "sky terrace" in state["context"]
        assert any("balustrade" in d["statement"].lower() for d in state["decisions"])
        # Unmatched titles are rejected on the wire too.
        assert post_nudge("Inbox - Outlook", url) is False
        # The workspace page and a demo drawing are served.
        with urllib.request.urlopen(f"{url}/workspace", timeout=5) as r:
            body = r.read()
            assert b"PROJECT WORKSPACE" in body and b"SIMULATED" in body
        with urllib.request.urlopen(f"{url}/drawings/Tanglin-Rise_L01_Fire-Plan.pdf", timeout=5) as r:
            assert r.read()[:5] == b"%PDF-"
    finally:
        server.shutdown()
