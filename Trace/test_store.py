import pytest
from store import (
    Decision, Episode, add_decision, add_episode, adopt_decision, connect,
    get_decision, get_episode, get_history, get_valid_asof, get_valid_decisions,
    init_db, link_supersession, reject_decision, set_project_code,
    supersede_decision, verify_audit_chain,
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


# ── project codes ────────────────────────────────────────────────────────────

def test_project_code_prefixes_ids():
    conn = _fresh()
    set_project_code(conn, "408213")
    a = add_decision(conn, Decision(statement="A"))
    b = add_decision(conn, Decision(statement="B"))
    assert a.id == "408213-D-001"
    assert b.id == "408213-D-002"


def test_coded_auto_id_skips_past_explicit_ids():
    conn = _fresh()
    set_project_code(conn, "408213")
    add_decision(conn, Decision(statement="imported", id="408213-D-007"))
    d = add_decision(conn, Decision(statement="next"))
    assert d.id == "408213-D-008"


def test_uncoded_store_keeps_bare_ids():
    conn = _fresh()
    assert add_decision(conn, Decision(statement="A")).id == "D-001"


# ── verdicts are state transitions ───────────────────────────────────────────

def test_reject_marks_the_proposal_rejected_never_deleted():
    conn = _fresh()
    add_decision(conn, Decision(statement="VE swap", status="proposed",
                                valid_from="2026-03-03T14:00Z"))
    d = reject_decision(conn, "D-001", rejected_at="2026-03-03T15:00Z")
    assert d.status == "rejected"
    assert d.valid_to == "2026-03-03T15:00:00Z"
    assert get_decision(conn, "D-001") is not None       # never deleted
    assert verify_audit_chain(conn)[0] is True           # the reject event chains on


def test_only_proposals_can_be_rejected():
    conn = _fresh()
    add_decision(conn, Decision(statement="in force"))
    with pytest.raises(ValueError):
        reject_decision(conn, "D-001")


def test_adopt_promotes_the_proposal_to_valid():
    conn = _fresh()
    add_decision(conn, Decision(statement="tenant cold room", status="proposed",
                                recorded_at="2026-04-02T16:00Z", valid_from="2026-04-02T16:00Z"))
    d = adopt_decision(conn, "D-001")
    assert d.status == "valid"
    assert [x.id for x in get_valid_decisions(conn)] == ["D-001"]


def test_rejected_proposal_never_appears_in_force_at_any_date():
    conn = _fresh()
    add_decision(conn, Decision(statement="VE swap", status="proposed",
                                recorded_at="2026-02-01T00:00Z", valid_from="2026-02-01T00:00Z"))
    reject_decision(conn, "D-001", rejected_at="2026-03-01T00:00Z")
    for when in ("2026-02-15T00:00Z", "2026-03-15T00:00Z", "2027-01-01T00:00Z"):
        assert get_valid_asof(conn, when) == [], when
    assert get_valid_decisions(conn) == []


# ── supersession guards ──────────────────────────────────────────────────────

def test_a_proposal_cannot_be_superseded_into_history():
    # A never-adopted proposal must not become retroactively "formerly in force".
    conn = _fresh()
    add_decision(conn, Decision(statement="proposal v1", status="proposed"))
    with pytest.raises(ValueError):
        supersede_decision(conn, "D-001", Decision(statement="proposal v2"))


def test_a_rejected_proposal_cannot_be_superseded_either():
    conn = _fresh()
    add_decision(conn, Decision(statement="proposal", status="proposed"))
    reject_decision(conn, "D-001")
    with pytest.raises(ValueError):
        supersede_decision(conn, "D-001", Decision(statement="revised proposal"))


def test_replacement_must_itself_be_in_force():
    conn = _fresh()
    add_decision(conn, Decision(statement="in force"))
    with pytest.raises(ValueError):
        supersede_decision(conn, "D-001", Decision(statement="pending", status="proposed"))


def test_link_supersession_closes_old_against_existing_new():
    conn = _fresh()
    add_decision(conn, Decision(statement="old", recorded_at="2026-01-01T00:00Z"))
    add_decision(conn, Decision(statement="new", recorded_at="2026-02-01T00:00Z",
                                valid_from="2026-02-01T00:00Z"))
    link_supersession(conn, "D-001", "D-002")
    old = get_decision(conn, "D-001")
    assert old.status == "superseded" and old.superseded_by == "D-002"
    assert old.valid_to == "2026-02-01T00:00:00Z"


# ── temporal consistency ─────────────────────────────────────────────────────

def test_backfilled_supersession_defaults_closure_to_replacement_knowledge():
    # superseded_at omitted on a backdated replacement: closure must default to
    # when the replacement was RECORDED, never "now" — otherwise the asof view
    # shows both versions in force for the whole backfill window.
    conn = _fresh()
    add_decision(conn, Decision(statement="v1", recorded_at="2026-01-01T00:00Z"))
    supersede_decision(conn, "D-001", Decision(
        statement="v2", recorded_at="2026-02-01T00:00Z", valid_from="2026-02-01T00:00Z"))
    assert [d.id for d in get_valid_asof(conn, "2026-03-01T00:00Z")] == ["D-002"]


def test_future_effective_supersession_keeps_old_in_force_today():
    # Decided today, effective in the future: the current view must keep the old
    # decision in force until the cutover — matching the bi-temporal view.
    conn = _fresh()
    add_decision(conn, Decision(statement="current spec", recorded_at="2026-01-01T00:00Z"))
    supersede_decision(conn, "D-001", Decision(
        statement="December spec", valid_from="2039-12-01T00:00Z"))
    assert [d.statement for d in get_valid_decisions(conn)] == ["current spec"]
    assert [d.statement for d in get_valid_asof(conn, "2039-12-02T00:00Z")] == ["December spec"]


# ── episodes (knowledge-base sources) ────────────────────────────────────────

def test_episode_round_trip_and_audit():
    conn = _fresh()
    e = add_episode(conn, Episode(body="## Meeting\nDecision: fix the facade.",
                                  path="inbox/meeting.md", frontmatter={"project": "demo"}))
    assert e.id == "E-001"
    got = get_episode(conn, "E-001")
    assert got.body.startswith("## Meeting")
    assert got.frontmatter == {"project": "demo"}
    assert verify_audit_chain(conn)[0] is True           # ingest is on the chain


def test_episode_dedupes_on_content_hash():
    conn = _fresh()
    a = add_episode(conn, Episode(body="same note", path="inbox/a.md"))
    b = add_episode(conn, Episode(body="same note", path="inbox/renamed.md"))
    assert a.id == b.id == "E-001"                       # re-saved/renamed: no duplicate
