import json
from types import SimpleNamespace

import bubble


def _fake_client(answer="ok"):
    create = lambda **kw: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=answer))])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def test_state_returns_project_record_and_project_list():
    s = json.loads(bubble.Api().state())
    statuses = {d["id"]: d["status"] for d in s["decisions"]}
    assert statuses["D-001"] == "valid"
    assert statuses["D-002"] == "proposed"
    assert statuses["D-004"] == "superseded"      # the never-delete chain is visible
    assert s["project"] == "tanglin-rise"
    assert [p["key"] for p in s["projects"]] == ["tanglin-rise", "kranji-hub", "maple-wharf"]


def test_each_project_has_its_own_grounded_record_no_bleed(monkeypatch):
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _capture_client("ok", calls))
    bubble.Api("kranji-hub").ask("what's the power situation?")
    ctx = "\n".join(m["content"] for m in calls[0]["messages"] if m["role"] == "system")
    assert "400 kVA" in ctx and "Kranji" in ctx
    assert "rainscreen" not in ctx                 # nothing from the other projects


def test_court_records_are_part_of_the_llm_context(monkeypatch):
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _capture_client("ok", calls))
    bubble.Api("maple-wharf").ask("was the ACM swap ever reviewed?")
    ctx = "\n".join(m["content"] for m in calls[0]["messages"] if m["role"] == "system")
    assert "COURT RECORD" in ctx and "reg 7(2)" in ctx


def test_greeting_gets_a_pointer_not_an_abstention():
    # "hi" must not hit the decision store (nor the LLM — no monkeypatch needed:
    # if this path tried to build a client it would raise without a key).
    out = json.loads(bubble.Api().ask("hi"))
    assert "why the non-combustible facade" in out["answer"]
    assert out["cited"] == []
    out2 = json.loads(bubble.Api().ask("hello, testing?"))
    assert out2["cited"] == []
    assert "No decision on record" not in out2["answer"]


def _capture_client(answer, calls):
    def create(**kw):
        calls.append(kw)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=answer))])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def test_meta_question_gets_a_real_answer_when_llm_available(monkeypatch):
    import openai
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _fake_client(
        "Trace is an ambient decision-memory agent; this demo watches Tanglin Rise."))
    out = json.loads(bubble.Api().ask("what is this project"))
    assert "Tanglin Rise" in out["answer"]
    assert out["cited"] == []


def test_falls_back_to_honest_abstention_without_a_key(monkeypatch):
    # No key -> degrade to the deterministic layer, never crash the UI.
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    out = json.loads(bubble.Api().ask("what is this project"))
    assert out["answer"] == "No decision on record; not yet decided."
    assert out["cited"] == []


def test_full_record_reaches_the_llm_regardless_of_question_wording(monkeypatch):
    # Typo robustness is structural: the LLM always receives the ENTIRE decision
    # record, so "why the facde claddng" needs no keyword match to be answerable.
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI",
                        lambda **kw: _capture_client("Because SCDF Cl 3.5.1 (D-001).", calls))
    out = json.loads(bubble.Api().ask("why the facde claddng??"))
    record = "\n".join(m["content"] for m in calls[0]["messages"] if m["role"] == "system")
    assert "D-001" in record and "D-002" in record          # full record in context
    assert "non-combustible mineral rainscreen" in record   # with rationale detail
    assert out["cited"] == ["D-001"]                        # cited ids parsed from the answer


def test_conversation_history_is_passed_to_followups(monkeypatch):
    # A memory agent's chat must remember the conversation: the second call's
    # messages include the first question and answer.
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI",
                        lambda **kw: _capture_client("The record cites SCDF Cl 3.5.1 (D-001).", calls))
    api = bubble.Api()
    api.ask("why the non-combustible facade cladding?")
    api.ask("show me the full clause")
    roles = [(m["role"], m["content"]) for m in calls[1]["messages"]]
    assert any(r == "user" and "non-combustible facade" in c for r, c in roles)
    assert any(r == "assistant" and "Cl 3.5.1" in c for r, c in roles)
    assert roles[-1] == ("user", "show me the full clause")


def test_ask_cites_decisions_mentioned_in_the_answer(monkeypatch):
    import openai
    monkeypatch.setattr(openai, "OpenAI",
                        lambda **kw: _fake_client("Locked (D-001); the ACM swap (D-002) was rejected. (D-999 ignored)"))
    out = json.loads(bubble.Api().ask("why the facade cladding and can we change it"))
    assert out["cited"] == ["D-001", "D-002"]  # D-999 not in the store -> filtered
    assert "D-001" in out["answer"]
