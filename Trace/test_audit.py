from store import connect, init_db, Decision, add_decision, supersede_decision, get_history
from audit import render_history


def _chain():
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(statement="Non-combustible facade", valid_from="2026-01-14T00:00Z"))
    supersede_decision(
        conn, "D-001",
        Decision(statement="PE-core ACP", valid_from="2026-03-03T00:00Z"),
        superseded_at="2026-03-03T00:00Z",
    )
    return get_history(conn, "D-001")


def test_render_history_shows_chain_and_status():
    text = render_history(_chain())
    assert "D-001" in text and "D-002" in text
    assert "superseded" in text
    assert "Non-combustible facade" in text
    assert "PE-core ACP" in text
    assert "(current)" in text          # D-002 has no valid_to


def test_render_empty_history_abstains():
    assert "No decision on record" in render_history([])


def _tamper_store():
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(statement="Non-combustible facade"))
    supersede_decision(conn, "D-001", Decision(statement="Upgraded spec"))
    return conn


def test_audit_chain_grows_and_verifies():
    from store import verify_audit_chain
    conn = _tamper_store()
    ok, n = verify_audit_chain(conn)
    assert ok is True
    assert n == 3  # add D-001, add D-002, supersede D-001
    from audit import render_chain_status
    assert "VERIFIED — 3 event(s)" in render_chain_status(conn)


def test_tampering_with_the_log_breaks_the_chain():
    from store import verify_audit_chain
    conn = _tamper_store()
    conn.execute("UPDATE audit_log SET payload = '{\"statement\":\"forged\"}' WHERE seq = 1")
    ok, seq = verify_audit_chain(conn)
    assert ok is False and seq == 1
    from audit import render_chain_status
    assert "BROKEN at event #1" in render_chain_status(conn)


def test_deleting_a_log_event_breaks_the_chain():
    from store import verify_audit_chain
    conn = _tamper_store()
    conn.execute("DELETE FROM audit_log WHERE seq = 2")
    ok, seq = verify_audit_chain(conn)
    assert ok is False and seq == 3  # the successor no longer links to seq 1


def test_court_verdicts_are_on_the_chain():
    from types import SimpleNamespace
    from capture import Captured
    from court import convene
    from store import verify_audit_chain
    conn = _tamper_store()
    fake = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(
        create=lambda **kw: SimpleNamespace(choices=[SimpleNamespace(
            message=SimpleNamespace(content="reasoning"))]))))
    ok_before, n_before = verify_audit_chain(conn)
    convene(conn, Captured(Decision(statement="Swap to PE-core ACP", discipline="facade"),
                           {"cladding_combustible": True}), client=fake)
    ok, n = verify_audit_chain(conn)
    assert ok is True and n == n_before + 1  # the verdict event chained on
