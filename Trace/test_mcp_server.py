"""The MCP server is the deterministic, keyless half of Trace: these tests call
the tool functions directly (no mcp package, no API key, no network) and one
guarded test builds the real FastMCP server to confirm the wiring."""
import pytest

import mcp_server
from scenarios import build_store


def test_list_projects_lists_the_portfolio_with_counts():
    projs = mcp_server.list_projects()
    keys = {p["key"] for p in projs}
    assert keys == {"tanglin-rise", "kranji-hub", "maple-wharf"}
    tanglin = next(p for p in projs if p["key"] == "tanglin-rise")
    assert tanglin["decisions"] >= 5 and "Tanglin" in tanglin["title"]


def test_list_decisions_keeps_superseded_and_rejected():
    out = mcp_server.list_decisions("tanglin-rise")
    by = {d["id"]: d for d in out["decisions"]}
    assert by["D-001"]["status"] == "valid"
    assert by["D-002"]["status"] == "rejected"         # the rejected VE proposal, preserved
    assert by["D-004"]["status"] == "superseded"      # never deleted
    assert by["D-004"]["superseded_by"] == "D-006"


def test_list_decisions_status_filter():
    valid = mcp_server.list_decisions("tanglin-rise", status="valid")
    assert valid["decisions"] and all(d["status"] == "valid" for d in valid["decisions"])
    assert "D-002" not in {d["id"] for d in valid["decisions"]}


def test_get_decision_returns_the_supersession_history():
    out = mcp_server.get_decision("tanglin-rise", "D-004")
    assert out["decision"]["status"] == "superseded"
    chain = [d["id"] for d in out["history"]]
    assert chain[0] == "D-004" and "D-006" in chain    # D-004 -> D-006


def test_decisions_asof_is_bitemporal():
    # As of 15 Jan, only D-001 was on record (D-003 recorded 20 Jan, D-004 28 Jan).
    early = {d["id"] for d in mcp_server.decisions_asof("tanglin-rise", "2026-01-15")["valid"]}
    assert "D-001" in early and "D-003" not in early and "D-004" not in early

    # As of 10 Feb the record showed the glass balustrade (D-004); the aluminium
    # replacement (D-006) was not yet recorded — knowledge time, not just validity.
    mid = {d["id"] for d in mcp_server.decisions_asof("tanglin-rise", "2026-02-10")["valid"]}
    assert "D-004" in mid and "D-006" not in mid

    # As of 1 Mar it has flipped: D-006 in force, D-004 superseded out.
    late = {d["id"] for d in mcp_server.decisions_asof("tanglin-rise", "2026-03-01")["valid"]}
    assert "D-006" in late and "D-004" not in late

    # Proposals are never "valid as of" anything.
    assert "D-002" not in late


def test_decisions_asof_bad_date_is_a_graceful_error():
    out = mcp_server.decisions_asof("tanglin-rise", "not-a-date")
    assert "error" in out


def test_check_compliance_flags_combustible_over_15m_with_clause_and_link():
    out = mcp_server.check_compliance(height_m=95, cladding_combustible=True)
    assert out["compliant"] is False
    v = out["violations"][0]
    assert v["rule_id"] == "SCDF-Cl3.5-noncombustible"
    assert "SCDF" in v["citation"]
    assert v["provision"] and v["url"].startswith("https://") and "scdf.gov.sg" in v["url"]
    assert any("s.9" in b for b in v["blast_radius"])


def test_check_compliance_passes_when_noncombustible():
    out = mcp_server.check_compliance(height_m=95, cladding_combustible=False)
    assert out["compliant"] is True and out["violations"] == []


def test_check_compliance_uk_jurisdiction_uses_the_uk_pack():
    out = mcp_server.check_compliance(height_m=62, cladding_combustible=True, jurisdiction="UK")
    assert out["compliant"] is False
    assert out["violations"][0]["rule_id"] == "UK-Reg7-2-combustible-ban"
    assert "legislation.gov.uk" in out["violations"][0]["url"]


def test_get_code_provision_returns_links_and_filters():
    allp = mcp_server.get_code_provision()
    assert allp and all(e["url"].startswith("https://") and e["provision"] for e in allp)
    uk = mcp_server.get_code_provision("reg 7")
    assert uk and all("legislation.gov.uk" in e["url"] for e in uk)


def test_verify_audit_chain_is_intact_for_a_built_store():
    out = mcp_server.verify_audit_chain("kranji-hub")
    assert out["intact"] is True and out["events"] > 0


def test_verify_audit_chain_detects_tampering(monkeypatch):
    conn = build_store("maple-wharf")
    monkeypatch.setitem(mcp_server._STORES, "maple-wharf", conn)  # tool reads this store
    conn.execute("UPDATE audit_log SET payload='{\"tampered\":1}' "
                 "WHERE seq = (SELECT MIN(seq) FROM audit_log)")
    conn.commit()
    out = mcp_server.verify_audit_chain("maple-wharf")
    assert out["intact"] is False and out["first_bad_seq"] >= 1


def test_court_records_carry_the_verdict_and_clause():
    out = mcp_server.court_records("tanglin-rise")
    rec = out["records"][0]
    assert rec["verdict"] == "REJECT" and rec["breaks_id"] == "D-001"
    assert "3.5.1" in rec["citation"]


def test_unknown_project_is_a_graceful_error():
    assert "error" in mcp_server.list_decisions("no-such-project")
    assert "error" in mcp_server.verify_audit_chain("no-such-project")


def test_build_server_registers_every_tool():
    pytest.importorskip("mcp")
    import anyio
    server = mcp_server.build_server()
    tools = anyio.run(server.list_tools)
    assert {t.name for t in tools} == {fn.__name__ for fn in mcp_server.TOOLS}
