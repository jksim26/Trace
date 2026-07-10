import json
from types import SimpleNamespace

from capture import Captured
from invalidate import check_invalidation, llm_premise_check, render_alert
from store import Decision, add_decision, connect, init_db


def _fake_client(payload: dict):
    text = json.dumps(payload)
    create = lambda **kw: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=text))])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def _store_with_d001():
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="Facade = non-combustible mineral rainscreen",
        discipline="facade",
        rationale="SCDF Cl 3.5: non-combustible mandated over 15 m",
        recorded_at="2026-01-14T00:00Z",
    ))
    return conn


def _combustible_facade():
    return Captured(
        Decision(statement="Swap facade to PE-core ACP", discipline="facade"),
        {"cladding_combustible": True},
    )


# The demo building's context — the rule-pack judges THIS project's facts, not
# a hardcoded building baked into the engine.
CTX = {"building": {"height_m": 95, "boundary_distance_m": 7.5}}


def test_combustible_facade_fires_alert_naming_prior():
    alerts = check_invalidation(_store_with_d001(), _combustible_facade(), context=CTX)
    assert len(alerts) == 1
    a = alerts[0]
    assert a.rule_id == "SCDF-Cl3.5-noncombustible"
    assert a.breaks is not None and a.breaks.id == "D-001"
    assert any("s.9" in b for b in a.blast_radius)


def test_compliant_change_fires_no_alert():
    ok = Captured(
        Decision(statement="Keep non-combustible rainscreen", discipline="facade"),
        {"cladding_combustible": False},
    )
    assert check_invalidation(_store_with_d001(), ok, context=CTX) == []


def test_no_attribute_no_alert():
    unrelated = Captured(Decision(statement="Core moved east", discipline="architecture"), {})
    assert check_invalidation(_store_with_d001(), unrelated, context=CTX) == []


def test_render_alert_has_key_facts():
    text = render_alert(check_invalidation(_store_with_d001(), _combustible_facade(), context=CTX)[0])
    assert "INVALIDATION ALERT" in text
    assert "PE-core ACP" in text
    assert "D-001" in text
    assert "SCDF Fire Code 2023 Cl 3.5" in text


def test_breaks_is_premise_aware_not_positional():
    """The old heuristic picked the LAST same-discipline decision; breaks must be
    the decision whose stated assumption the new decision actually contradicts,
    with the specific premise named."""
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="Facade = non-combustible mineral rainscreen",
        discipline="facade",
        assumptions=["combustible external cladding is prohibited over 15 m",
                     "building height stays above 15 m"],
        recorded_at="2026-01-14T00:00Z"))
    # A later same-discipline decision with unrelated assumptions — the old
    # positional heuristic would (wrongly) pick this one.
    add_decision(conn, Decision(
        statement="Facade access gantry on level 12",
        discipline="facade",
        assumptions=["gantry loads are within the slab capacity"],
        recorded_at="2026-02-01T00:00Z"))
    alerts = check_invalidation(conn, _combustible_facade(), context=CTX)
    assert len(alerts) == 1
    assert alerts[0].breaks.id == "D-001"
    assert alerts[0].broken_premise == "combustible external cladding is prohibited over 15 m"
    assert 'premise broken: "combustible external cladding is prohibited' in render_alert(alerts[0])


def _store_with_power_budget():
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="Chiller plant sized to 400 kVA",
        discipline="mep",
        assumptions=["site power budget is 400 kVA"],
        recorded_at="2026-01-14T00:00Z"))
    return conn


def test_llm_premise_check_fires_when_rules_are_silent():
    # No rule-pack attribute is involved — the general LLM half must catch it.
    new = Captured(Decision(statement="Increase chiller plant to 600 kVA", discipline="mep"), {})
    client = _fake_client({"breaks": True,
                           "premise": "site power budget is 400 kVA",
                           "why": "600 kVA exceeds the stated 400 kVA budget."})
    alerts = check_invalidation(_store_with_power_budget(), new, client=client)
    assert len(alerts) == 1
    assert alerts[0].source == "llm"
    assert alerts[0].rule_id == "LLM-PREMISE"
    assert alerts[0].breaks.id == "D-001"
    assert alerts[0].broken_premise == "site power budget is 400 kVA"


def test_llm_premise_check_negative_verdict_is_silent():
    new = Captured(Decision(statement="Repaint the chiller plant room", discipline="mep"), {})
    client = _fake_client({"breaks": False, "premise": "", "why": "No premise affected."})
    assert check_invalidation(_store_with_power_budget(), new, client=client) == []


def test_rule_hit_short_circuits_the_llm():
    # client=object() proves the LLM is never consulted when the rule-pack fires.
    alerts = check_invalidation(_store_with_d001(), _combustible_facade(), client=object(), context=CTX)
    assert len(alerts) == 1
    assert alerts[0].source == "rule"


def test_llm_premise_check_skips_decisions_without_keyword_overlap():
    # Candidate narrowing: nothing shares a content word -> no LLM call at all.
    new = Captured(Decision(statement="Lobby terrazzo pattern approved", discipline="architecture"), {})
    assert llm_premise_check(_store_with_power_budget(), new, client=object()) == []


def test_no_context_means_building_rules_stay_silent():
    # A project with no stated building context must not inherit another
    # building's height: the fire rules simply do not engage.
    assert check_invalidation(_store_with_d001(), _combustible_facade()) == []
