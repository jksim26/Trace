from court import get_court_records
from recall import retrieve
from scenarios import PROJECTS, build_store
from store import get_all_decisions, get_valid_asof


def test_every_project_gives_trace_something_to_remember():
    # Each store carries the full memory story: valid decisions, a rejected
    # proposal (preserved), a superseded chain (never deleted), a court record.
    for key in PROJECTS:
        conn = build_store(key)
        ds = get_all_decisions(conn)
        assert len(ds) >= 5, key
        statuses = {d.status for d in ds}
        assert {"valid", "proposed", "superseded"} <= statuses, key
        records = get_court_records(conn)
        assert len(records) == 1 and records[0]["verdict"] == "REJECT", key
        assert all(d.assumptions for d in ds if d.status == "valid"), key


def test_time_travel_works_on_scenario_data():
    conn = build_store("maple-wharf")
    # Before the two-staircase supersession, single-stair (D-003) was the record.
    before = [d.id for d in get_valid_asof(conn, "2026-02-01T00:00Z")]
    assert "D-003" in before and "D-005" not in before
    after = [d.id for d in get_valid_asof(conn, "2026-04-01T00:00Z")]
    assert "D-005" in after and "D-003" not in after


def test_retrieval_finds_the_right_memory_per_project():
    packed, _ = retrieve(build_store("kranji-hub"), "what is the site power budget")
    assert any("400 kVA" in d.statement or "400 kVA" in " ".join(d.assumptions) for d in packed)
    packed, _ = retrieve(build_store("maple-wharf"), "why the terracotta rainscreen facade")
    assert any(d.id == "D-001" for d in packed)
