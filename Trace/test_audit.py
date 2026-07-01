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
