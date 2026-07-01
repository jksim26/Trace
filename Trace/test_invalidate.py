from capture import Captured
from invalidate import check_invalidation, render_alert
from store import Decision, add_decision, connect, init_db


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


def test_combustible_facade_fires_alert_naming_prior():
    alerts = check_invalidation(_store_with_d001(), _combustible_facade())
    assert len(alerts) == 1
    a = alerts[0]
    assert a.rule_id == "SCDF-Cl3.5-noncombustible"
    assert a.breaks is not None and a.breaks.id == "D-001"
    assert "qp.s9_personal_liability" in a.blast_radius


def test_compliant_change_fires_no_alert():
    ok = Captured(
        Decision(statement="Keep non-combustible rainscreen", discipline="facade"),
        {"cladding_combustible": False},
    )
    assert check_invalidation(_store_with_d001(), ok) == []


def test_no_attribute_no_alert():
    unrelated = Captured(Decision(statement="Core moved east", discipline="architecture"), {})
    assert check_invalidation(_store_with_d001(), unrelated) == []


def test_render_alert_has_key_facts():
    text = render_alert(check_invalidation(_store_with_d001(), _combustible_facade())[0])
    assert "INVALIDATION ALERT" in text
    assert "PE-core ACP" in text
    assert "D-001" in text
    assert "SCDF Fire Code 2023 Cl 3.5" in text
