import json

import mcp_tools
from mcp_tools import CaptureDecision, CheckInvalidation, RecallDecisions, SupersedeDecision
from store import Decision, add_decision


def _seed_d001():
    mcp_tools.reset_store()
    add_decision(mcp_tools._get_conn(), Decision(
        statement="Facade = non-combustible mineral rainscreen",
        discipline="facade",
        rationale="SCDF Cl 3.5 mandates non-combustible over 15 m",
        recorded_at="2026-01-14T00:00Z",
    ))


def test_tools_have_qwen_agent_names():
    assert CaptureDecision().name == "capture_decision"
    assert CheckInvalidation().name == "check_invalidation"
    assert RecallDecisions().name == "recall_decisions"
    assert SupersedeDecision().name == "supersede_decision"


def test_check_invalidation_tool_reports_conflict():
    _seed_d001()
    out = json.loads(CheckInvalidation().call(json.dumps(
        {"statement": "Swap to PE-core ACP", "cladding_combustible": True})))
    assert out["conflict"] is True
    assert "SCDF Fire Code 2023 Cl 3.5" in out["alerts"][0]


def test_check_invalidation_tool_no_conflict_when_noncombustible():
    _seed_d001()
    out = json.loads(CheckInvalidation().call(json.dumps(
        {"statement": "Keep mineral rainscreen", "cladding_combustible": False})))
    assert out["conflict"] is False


def test_recall_tool_abstains_without_api():
    _seed_d001()
    out = json.loads(RecallDecisions().call(json.dumps(
        {"question": "did we decide the planter balustrade material"})))
    assert out["abstained"] is True
    assert "No decision on record" in out["answer"]


def test_supersede_tool_preserves_chain():
    _seed_d001()
    out = json.loads(SupersedeDecision().call(json.dumps(
        {"old_id": "D-001", "new_statement": "Facade = fibre-cement panel (non-combustible)"})))
    assert out["new_id"] == "D-002"
    assert [c["id"] for c in out["chain"]] == ["D-001", "D-002"]
