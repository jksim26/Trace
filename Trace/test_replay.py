"""The offline demo safety net: `python cli.py --offline` must run the whole
four-scene demo end-to-end with NO network and NO API key. This is the test a
judge's machine effectively runs."""
import json

import cli
from court import get_court_records
from replay import FIXTURE, ReplayClient
from store import get_all_decisions


def test_fixture_is_well_formed():
    entries = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert len(entries) >= 6  # capture x2, court roles x3, recall x1
    assert entries[0]["kind"] == "tool_calls"
    assert entries[1]["kind"] == "tool_calls"
    assert all(e["kind"] in ("tool_calls", "content") for e in entries)
    # Scene 2's proposal must carry the combustible attribute or the alert
    # (the demo's centrepiece) cannot fire.
    assert entries[1]["calls"][0]["arguments"]["cladding_combustible"] is True


def test_offline_demo_runs_end_to_end_with_no_network():
    conn = cli.run(pause=False, client=ReplayClient())

    decisions = {d.id: d for d in get_all_decisions(conn)}
    assert decisions["D-001"].status == "valid"
    assert decisions["D-002"].status == "proposed"   # preserved, never deleted

    records = get_court_records(conn)
    assert len(records) == 1
    assert records[0]["verdict"] == "REJECT"
    assert records[0]["breaks_id"] == "D-001"
    assert records[0]["rationale"]


def test_replay_client_raises_clearly_when_exhausted():
    client = ReplayClient()
    client._queue = []
    try:
        client.chat.completions.create(model="x", messages=[])
        assert False, "expected RuntimeError"
    except RuntimeError as e:
        assert "--record" in str(e) or "record" in str(e)
