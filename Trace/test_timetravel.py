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


def test_asof_retroactive_supersession_shows_what_was_known():
    """The liability question itself ('what did you know, and when' — Building
    Control Act s.9 turns on it): a supersession recorded on 1 Mar but
    BACKDATED (valid_from 1 Feb — the norm in AEC, where decisions are minuted
    after the fact) must not erase what the record showed mid-February.
    """
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="Non-combustible facade", discipline="facade",
        recorded_at="2026-01-01T00:00Z", valid_from="2026-01-01T00:00Z"))
    supersede_decision(
        conn, "D-001",
        Decision(statement="Revised facade spec", discipline="facade",
                 recorded_at="2026-03-01T00:00Z", valid_from="2026-02-01T00:00Z"),
        superseded_at="2026-03-01T00:00Z")
    # On 15 Feb the swap was not yet on record: D-001 is what the team knew.
    assert [d.id for d in get_valid_asof(conn, "2026-02-15T00:00Z")] == ["D-001"]
    # Once the supersession is on record, the replacement wins.
    assert [d.id for d in get_valid_asof(conn, "2026-03-15T00:00Z")] == ["D-002"]


def test_asof_mixed_timestamp_precisions_compare_chronologically():
    """Minute-precision and second-precision inputs must not mis-sort: as a raw
    string "T00:00Z" compares AFTER "T00:00:00Z". The store canonicalizes on
    write, so the same instant matches regardless of the caller's precision.
    """
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="A", recorded_at="2026-01-14T11:42Z", valid_from="2026-01-14T11:42Z"))
    assert [d.statement for d in get_valid_asof(conn, "2026-01-14T11:42:00Z")] == ["A"]
    assert [d.statement for d in get_valid_asof(conn, "2026-01-14T11:41:59Z")] == []
