import pytest
from store import (
    connect, init_db, Decision, add_decision, get_decision,
    get_valid_decisions, get_valid_asof, supersede_decision, get_history,
    set_status, get_resubmission_chain,
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
    assert got.valid_from == "2026-01-14T11:45:00Z"  # canonicalized to second precision


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
    assert old.valid_to == "2026-03-01T00:00:00Z"      # canonicalized
    assert old.superseded_at == "2026-03-01T00:05:00Z"  # canonicalized
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


def test_double_supersede_raises_no_forked_chain():
    conn = _fresh()
    add_decision(conn, Decision(statement="v1"))
    supersede_decision(conn, "D-001", Decision(statement="v2"))
    with pytest.raises(ValueError):
        supersede_decision(conn, "D-001", Decision(statement="v3-fork"))


def test_auto_id_skips_past_explicit_ids():
    # COUNT-based ids collided with any explicitly-supplied id; MAX-based must not.
    conn = _fresh()
    add_decision(conn, Decision(statement="imported", id="D-007"))
    d = add_decision(conn, Decision(statement="next"))
    assert d.id == "D-008"


def test_timestamps_canonicalized_on_write():
    # Minute-precision input is stored at second precision so string comparison
    # in SQL is chronological.
    conn = _fresh()
    d = add_decision(conn, Decision(statement="A", recorded_at="2026-01-14T11:45Z"))
    got = get_decision(conn, d.id)
    assert got.recorded_at == "2026-01-14T11:45:00Z"
    assert got.valid_from == "2026-01-14T11:45:00Z"


def test_get_history_walks_full_chain():
    conn = _fresh()
    add_decision(conn, Decision(statement="v1"))
    supersede_decision(conn, "D-001", Decision(statement="v2"))
    supersede_decision(conn, "D-002", Decision(statement="v3"))
    chain = get_history(conn, "D-001")
    assert [d.id for d in chain] == ["D-001", "D-002", "D-003"]
    assert [d.statement for d in chain] == ["v1", "v2", "v3"]


def test_set_status_updates_and_audits():
    conn = _fresh()
    d = add_decision(conn, Decision(statement="proposal", status="proposed"))
    updated = set_status(conn, d.id, "rejected")
    assert updated.status == "rejected"
    assert get_decision(conn, d.id).status == "rejected"
    from store import verify_audit_chain
    ok, n = verify_audit_chain(conn)
    assert ok and n == 2  # add + status_change, both on the chain


def test_set_status_unknown_status_rejected():
    conn = _fresh()
    d = add_decision(conn, Decision(statement="proposal", status="proposed"))
    with pytest.raises(ValueError):
        set_status(conn, d.id, "not-a-real-status")


def test_set_status_unknown_decision_raises():
    conn = _fresh()
    with pytest.raises(ValueError):
        set_status(conn, "D-404", "valid")


def test_get_valid_asof_excludes_rejected_as_well_as_proposed():
    conn = _fresh()
    add_decision(conn, Decision(statement="A", recorded_at="2026-01-01T00:00Z",
                                valid_from="2026-01-01T00:00Z"))
    add_decision(conn, Decision(statement="rejected swap", status="rejected",
                                recorded_at="2026-01-02T00:00Z", valid_from="2026-01-02T00:00Z"))
    ids = [d.id for d in get_valid_asof(conn, "2026-06-01T00:00Z")]
    assert ids == ["D-001"]


def test_resubmits_field_round_trips():
    conn = _fresh()
    rejected = add_decision(conn, Decision(statement="v1 rejected", status="rejected"))
    retry = add_decision(conn, Decision(statement="v2 retry", resubmits=rejected.id))
    got = get_decision(conn, retry.id)
    assert got.resubmits == rejected.id


def test_get_resubmission_chain_walks_retries_latest_first():
    conn = _fresh()
    first = add_decision(conn, Decision(statement="attempt 1", status="rejected"))
    second = add_decision(conn, Decision(statement="attempt 2", status="rejected",
                                         resubmits=first.id))
    third = add_decision(conn, Decision(statement="attempt 3", resubmits=second.id))
    chain = get_resubmission_chain(conn, third.id)
    assert [d.id for d in chain] == [third.id, second.id, first.id]


def test_get_resubmission_chain_single_decision_has_no_retries():
    conn = _fresh()
    d = add_decision(conn, Decision(statement="only attempt"))
    assert [x.id for x in get_resubmission_chain(conn, d.id)] == [d.id]
