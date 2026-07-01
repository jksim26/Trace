from store import Decision, add_decision, connect, get_valid_asof, init_db, supersede_decision


def _store():
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="Non-combustible facade", discipline="facade",
        recorded_at="2026-01-14T00:00Z", valid_from="2026-01-14T00:00Z"))
    supersede_decision(
        conn, "D-001",
        Decision(statement="Upgraded non-combustible facade", discipline="facade",
                 recorded_at="2026-03-01T00:00Z", valid_from="2026-03-01T00:00Z"),
        superseded_at="2026-03-01T00:00Z")
    return conn


def test_asof_before_supersession_shows_the_original():
    assert [d.id for d in get_valid_asof(_store(), "2026-02-01T00:00Z")] == ["D-001"]


def test_asof_after_supersession_shows_the_replacement():
    assert [d.id for d in get_valid_asof(_store(), "2026-04-01T00:00Z")] == ["D-002"]


def test_asof_before_anything_recorded_is_empty():
    assert get_valid_asof(_store(), "2026-01-01T00:00Z") == []
