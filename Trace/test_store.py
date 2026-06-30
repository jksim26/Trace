import pytest
from store import (
    connect, init_db, Decision, add_decision, get_decision,
    get_valid_decisions, supersede_decision, get_history,
)


def _fresh():
    conn = connect(":memory:")
    init_db(conn)
    return conn


def test_init_creates_decisions_table():
    conn = _fresh()
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='decisions'"
    ).fetchone()
    assert row is not None


def test_round_trip_preserves_fields():
    conn = _fresh()
    d = Decision(
        statement="Facade = terracotta on A2 mineral wool",
        discipline="facade",
        author=["R. Wells", "P. Desai"],
        assumptions=["building remains an HRB (>18m)"],
        importance=5,
        recorded_at="2026-01-14T11:45Z",
    )
    add_decision(conn, d)
    got = get_decision(conn, d.id)
    assert got.statement == "Facade = terracotta on A2 mineral wool"
    assert got.author == ["R. Wells", "P. Desai"]
    assert got.assumptions == ["building remains an HRB (>18m)"]
    assert got.status == "valid"
    assert got.valid_to is None
    assert got.valid_from == "2026-01-14T11:45Z"


def test_auto_id_sequence():
    conn = _fresh()
    a = add_decision(conn, Decision(statement="A"))
    b = add_decision(conn, Decision(statement="B"))
    assert a.id == "D-001"
    assert b.id == "D-002"


def test_get_missing_returns_none():
    conn = _fresh()
    assert get_decision(conn, "D-999") is None


def test_get_valid_lists_only_currently_valid():
    conn = _fresh()
    add_decision(conn, Decision(statement="A", recorded_at="2026-01-01T00:00Z"))
    add_decision(conn, Decision(statement="B", recorded_at="2026-01-02T00:00Z"))
    valid = get_valid_decisions(conn)
    assert [d.statement for d in valid] == ["A", "B"]


def test_supersede_preserves_old_row():
    conn = _fresh()
    add_decision(conn, Decision(statement="terracotta", recorded_at="2026-01-01T00:00Z"))
    new = supersede_decision(
        conn,
        "D-001",
        Decision(statement="ACM cladding", valid_from="2026-03-01T00:00Z"),
        superseded_at="2026-03-01T00:05Z",
    )
    old = get_decision(conn, "D-001")
    assert old is not None
    assert old.status == "superseded"
    assert old.superseded_by == "D-002"
    assert old.valid_to == "2026-03-01T00:00Z"
    assert old.superseded_at == "2026-03-01T00:05Z"
    assert new.id == "D-002" and new.status == "valid" and new.valid_to is None


def test_supersede_removes_old_from_valid_set():
    conn = _fresh()
    add_decision(conn, Decision(statement="terracotta", recorded_at="2026-01-01T00:00Z"))
    supersede_decision(conn, "D-001", Decision(statement="ACM", valid_from="2026-03-01T00:00Z"))
    assert [d.id for d in get_valid_decisions(conn)] == ["D-002"]


def test_supersede_unknown_id_raises():
    conn = _fresh()
    with pytest.raises(ValueError):
        supersede_decision(conn, "D-404", Decision(statement="x"))


def test_get_history_walks_full_chain():
    conn = _fresh()
    add_decision(conn, Decision(statement="v1"))
    supersede_decision(conn, "D-001", Decision(statement="v2"))
    supersede_decision(conn, "D-002", Decision(statement="v3"))
    chain = get_history(conn, "D-001")
    assert [d.id for d in chain] == ["D-001", "D-002", "D-003"]
    assert [d.statement for d in chain] == ["v1", "v2", "v3"]
