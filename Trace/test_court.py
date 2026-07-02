from types import SimpleNamespace

from capture import Captured
from court import convene, get_court_records, render_verdict
from store import Decision, add_decision, connect, init_db


def _fake_client(text="because SCDF Cl 3.5"):
    create = lambda **kw: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=text))])
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


def test_court_rejects_on_conflict_with_full_reasoning():
    v = convene(_store_with_d001(), _combustible(), client=_fake_client())
    assert v.conflict is True
    assert v.verdict == "REJECT"
    assert v.breaks == "D-001"
    assert v.for_argument and v.against_argument and v.rationale
    assert "VERDICT: REJECT" in render_verdict(v)


def test_court_allows_when_no_conflict_without_calling_llm():
    ok = Captured(Decision(statement="Keep non-combustible rainscreen", discipline="facade"),
                  {"cladding_combustible": False})
    v = convene(_store_with_d001(), ok, client=object())  # object() proves no LLM call
    assert v.conflict is False and v.verdict == "ALLOW"


def test_court_persists_reject_verdict_to_the_record():
    conn = _store_with_d001()
    convene(conn, _combustible(), client=_fake_client())
    records = get_court_records(conn)
    assert len(records) == 1
    r = records[0]
    assert r["verdict"] == "REJECT"
    assert r["breaks_id"] == "D-001"
    assert r["rationale"]  # the judge's reasoning is on the record
    assert r["created_at"]


def test_court_persists_allow_verdict_too():
    conn = _store_with_d001()
    ok = Captured(Decision(statement="Keep non-combustible rainscreen", discipline="facade"),
                  {"cladding_combustible": False})
    convene(conn, ok, client=object())
    records = get_court_records(conn)
    assert len(records) == 1
    assert records[0]["verdict"] == "ALLOW"
