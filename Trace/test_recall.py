from recall import recall_decisions, retrieve
from store import Decision, add_decision, connect, get_all_decisions, init_db


def _store_facade():
    conn = connect(":memory:")
    init_db(conn)
    add_decision(conn, Decision(
        statement="Facade = non-combustible mineral rainscreen above 15 m",
        discipline="facade",
        rationale="SCDF Cl 3.5 mandates non-combustible cladding over 15 m",
        recorded_at="2026-01-14T00:00Z",
    ))
    return conn


def test_retrieve_finds_relevant_and_costs_tokens():
    packed, used = retrieve(_store_facade(), "why the non-combustible facade cladding")
    assert [d.id for d in packed] == ["D-001"]
    assert used > 0


def test_retrieve_respects_budget():
    packed, _ = retrieve(_store_facade(), "facade non-combustible", budget=1)
    assert packed == []


def test_recall_abstains_when_nothing_relevant():
    # client=object() proves the LLM is never called on the abstain path.
    r = recall_decisions(_store_facade(), "did we decide the sky-terrace planter material", client=object())
    assert r.abstained is True
    assert "No decision on record" in r.answer
    assert r.cited == []


def test_abstention_reports_real_candidate_count():
    # Abstention can also happen because the budget is too tight to pack a match;
    # the meter must report the real candidate count, not pretend nothing matched.
    # client=object() proves the LLM is never called on this path either.
    r = recall_decisions(_store_facade(), "why the non-combustible facade cladding",
                         budget=1, client=object())
    assert r.abstained is True
    assert r.candidates == 1


def test_get_all_decisions_returns_everything_incl_nonvalid():
    conn = _store_facade()
    add_decision(conn, Decision(statement="Proposed cheaper panel", discipline="facade", status="proposed"))
    assert [d.id for d in get_all_decisions(conn)] == ["D-001", "D-002"]


def _fake_client(answer="answer"):
    from types import SimpleNamespace
    create = lambda **kw: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=answer))])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def test_recall_surfaces_rejected_proposal_as_context():
    conn = _store_facade()
    add_decision(conn, Decision(statement="Switch facade cladding to combustible PE-core ACP",
                                discipline="facade", status="proposed", rationale="cost saving"))
    r = recall_decisions(conn, "why the facade cladding and can we change it",
                         client=_fake_client("You cannot (D-001); the PE-core swap was rejected (D-002)."))
    assert r.abstained is False
    assert r.cited == ["D-001", "D-002"]
