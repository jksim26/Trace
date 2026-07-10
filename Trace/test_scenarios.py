from court import get_court_records
from recall import retrieve
from scenarios import PROJECTS, build_store
from store import get_all_decisions, get_valid_asof


def test_every_project_gives_trace_something_to_remember():
    # Each store carries the full memory story: valid decisions, a rejected
    # proposal (a REAL 'rejected' status, preserved), a superseded chain (never
    # deleted), a court record whose fate matches the row.
    for key in PROJECTS:
        conn = build_store(key)
        ds = get_all_decisions(conn)
        assert len(ds) >= 5, key
        statuses = {d.status for d in ds}
        assert {"valid", "rejected", "superseded"} <= statuses, key
        records = get_court_records(conn)
        assert len(records) == 1 and records[0]["verdict"] == "REJECT", key
        rejected = {d.id for d in ds if d.status == "rejected"}
        assert records[0]["proposal_id"] in rejected, key   # verdict joins the rejected row
        assert all(d.assumptions for d in ds if d.status == "valid"), key


def test_every_project_is_singapore_with_a_six_digit_code():
    for key, meta in PROJECTS.items():
        assert "Singapore" in meta["title"] or "Singapore" in meta["blurb"], key
        assert meta["code"].isdigit() and len(meta["code"]) == 6, key
        conn = build_store(key)
        assert all(d.id.startswith(meta["code"] + "-D-") for d in get_all_decisions(conn)), key


def test_codes_are_unique_so_ids_cannot_collide_across_projects():
    codes = [meta["code"] for meta in PROJECTS.values()]
    assert len(set(codes)) == len(codes)
    all_ids = [d.id for key in PROJECTS for d in get_all_decisions(build_store(key))]
    assert len(set(all_ids)) == len(all_ids)


def test_time_travel_works_on_scenario_data():
    conn = build_store("pearl-vista")
    # Before the permanent repair, the interim netting (D-004) was the record.
    before = [d.id for d in get_valid_asof(conn, "2026-03-01T00:00Z")]
    assert "629481-D-004" in before and "629481-D-005" not in before
    after = [d.id for d in get_valid_asof(conn, "2026-06-01T00:00Z")]
    assert "629481-D-005" in after and "629481-D-004" not in after
    # The rejected drone-only proposal is never in force at any date.
    assert "629481-D-002" not in before and "629481-D-002" not in after


def test_retrieval_finds_the_right_memory_per_project():
    packed, _ = retrieve(build_store("kranji-hub"), "what is the site power budget")
    assert any("400 kVA" in d.statement or "400 kVA" in " ".join(d.assumptions) for d in packed)
    packed, _ = retrieve(build_store("pearl-vista"), "why the facade inspection programme")
    assert any(d.id == "629481-D-001" for d in packed)
