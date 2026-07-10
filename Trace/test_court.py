import json
from types import SimpleNamespace

from capture import Captured
from court import convene, get_court_records, render_verdict
from store import Decision, add_decision, connect, get_decision, get_valid_decisions, init_db

# The demo building context the rule-pack judges against (95 m tower).
CTX = {"building": {"height_m": 95, "boundary_distance_m": 7.5}}


def _fake_client(text="because SCDF Cl 3.5"):
    create = lambda **kw: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=text))])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def _scripted_client(texts):
    """Returns each canned text in turn — proposer, guardian, judge."""
    queue = list(texts)
    create = lambda **kw: SimpleNamespace(choices=[SimpleNamespace(
        message=SimpleNamespace(content=queue.pop(0)))])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def _store_with_d001():
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="Facade cladding = non-combustible mineral rainscreen",
        discipline="facade", rationale="SCDF Cl 3.5 mandates non-combustible over 15 m",
        recorded_at="2026-01-14T00:00Z"))
    return conn


def _combustible():
    return Captured(Decision(statement="Swap facade to PE-core ACP", discipline="facade"),
                    {"cladding_combustible": True})


def test_court_rejects_on_rule_conflict_with_full_reasoning():
    v = convene(_store_with_d001(), _combustible(), client=_fake_client(), context=CTX)
    assert v.conflict is True
    assert v.verdict == "REJECT"
    assert v.breaks == "D-001"
    assert v.for_argument and v.against_argument and v.rationale
    assert "VERDICT: REJECT" in render_verdict(v)


def test_reject_verdict_marks_the_proposal_rejected_on_the_record():
    # The verdict is a real state transition, not just prose: the judged
    # proposal is stored and its fate lands on its row.
    conn = _store_with_d001()
    cap = _combustible()
    convene(conn, cap, client=_fake_client(), context=CTX)
    proposal = get_decision(conn, cap.decision.id)
    assert proposal is not None
    assert proposal.status == "rejected"
    assert [d.id for d in get_valid_decisions(conn)] == ["D-001"]  # unchanged in force


def test_court_allows_when_no_conflict():
    conn = _store_with_d001()
    ok = Captured(Decision(statement="Keep non-combustible rainscreen", discipline="facade"),
                  {"cladding_combustible": False})
    v = convene(conn, ok, client=None, context=CTX)  # no client: rule-silent stays silent
    assert v.conflict is False and v.verdict == "ALLOW"
    # ALLOW is a transition too: the proposal is adopted into force.
    assert ok.decision.id in {d.id for d in get_valid_decisions(conn)}


def test_court_persists_reject_verdict_to_the_record():
    conn = _store_with_d001()
    cap = _combustible()
    convene(conn, cap, client=_fake_client(), context=CTX)
    records = get_court_records(conn)
    assert len(records) == 1
    r = records[0]
    assert r["verdict"] == "REJECT"
    assert r["breaks_id"] == "D-001"
    assert r["proposal_id"] == cap.decision.id  # the verdict joins back to the judged row
    assert r["rationale"]  # the judge's reasoning is on the record
    assert r["created_at"]


def test_court_persists_allow_verdict_too():
    conn = _store_with_d001()
    ok = Captured(Decision(statement="Keep non-combustible rainscreen", discipline="facade"),
                  {"cladding_combustible": False})
    convene(conn, ok, client=None, context=CTX)
    records = get_court_records(conn)
    assert len(records) == 1
    assert records[0]["verdict"] == "ALLOW"


def _store_with_power_budget():
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="Chiller plant sized to 400 kVA",
        discipline="mep",
        assumptions=["site power budget is 400 kVA"],
        recorded_at="2026-01-14T00:00Z"))
    return conn


def test_rule_silent_premise_break_reaches_the_court_via_llm_check():
    # No fire rule is involved — convene must still consult the LLM premise
    # check (the general half) rather than waving the proposal through.
    conn = _store_with_power_budget()
    cap = Captured(Decision(statement="Increase chiller plant to 600 kVA", discipline="mep"), {})
    client = _scripted_client([
        json.dumps({"breaks": True, "premise": "site power budget is 400 kVA",
                    "why": "600 kVA exceeds the stated 400 kVA budget."}),  # premise check
        "The tenant needs more cooling.",                                     # proposer
        "It falsifies D-001's 400 kVA premise.",                              # guardian
        json.dumps({"verdict": "REJECT",
                    "rationale": "600 kVA falsifies D-001's committed 400 kVA supply."}),  # judge
    ])
    v = convene(conn, cap, client=client)
    assert v.conflict is True and v.verdict == "REJECT"
    assert get_decision(conn, cap.decision.id).status == "rejected"


def test_open_judge_can_genuinely_allow_and_supersede():
    # On probabilistic (LLM) evidence the judge DECIDES — an ALLOW adopts the
    # proposal and supersedes the decision whose premise it displaced.
    conn = _store_with_power_budget()
    cap = Captured(Decision(statement="Increase chiller plant to 600 kVA now that the supply "
                                      "upgrade is committed", discipline="mep"), {})
    client = _scripted_client([
        json.dumps({"breaks": True, "premise": "site power budget is 400 kVA",
                    "why": "The plant was sized on 400 kVA."}),               # premise check
        "The supply upgrade to 800 kVA is contractually committed.",          # proposer
        "The 400 kVA premise is falsified.",                                  # guardian
        json.dumps({"verdict": "ALLOW",
                    "rationale": "The premise did break — and the upgrade replaces it."}),  # judge
    ])
    v = convene(conn, cap, client=client)
    assert v.conflict is True and v.verdict == "ALLOW"
    new = get_decision(conn, cap.decision.id)
    old = get_decision(conn, "D-001")
    assert new.status == "valid"
    assert old.status == "superseded" and old.superseded_by == new.id
    assert [d.id for d in get_valid_decisions(conn)] == [new.id]


def test_unparseable_open_ruling_falls_back_to_reject():
    # With live evidence that a premise broke, a garbled ruling must hold the
    # proposal (REJECT), never wave it into force.
    conn = _store_with_power_budget()
    cap = Captured(Decision(statement="Increase chiller plant to 600 kVA", discipline="mep"), {})
    client = _scripted_client([
        json.dumps({"breaks": True, "premise": "site power budget is 400 kVA", "why": "over budget"}),
        "proposer prose", "guardian prose", "NOT JSON AT ALL",
    ])
    v = convene(conn, cap, client=client)
    assert v.verdict == "REJECT"
    assert get_decision(conn, cap.decision.id).status == "rejected"
