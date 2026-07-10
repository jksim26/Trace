import json
from types import SimpleNamespace

import pytest

import bubble


@pytest.fixture(autouse=True)
def _fresh_conversation():
    bubble._HISTORY.clear()
    yield
    bubble._HISTORY.clear()


def _fake_client(answer="ok"):
    create = lambda **kw: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=answer))])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def test_state_returns_project_record_and_project_list():
    s = json.loads(bubble.Api().state())
    statuses = {d["id"]: d["status"] for d in s["decisions"]}
    assert statuses["408213-D-001"] == "valid"
    assert statuses["408213-D-002"] == "rejected"          # the court's fate, on the row
    assert statuses["408213-D-004"] == "superseded"        # the never-delete chain is visible
    assert s["project"] == "tanglin-rise"
    assert [p["key"] for p in s["projects"]] == ["tanglin-rise", "kranji-hub", "pearl-vista"]


def test_one_memory_spans_all_projects_with_the_viewed_one_as_default(monkeypatch):
    # Trace is one agent with one memory: viewing Pearl Vista must not hide
    # Tanglin Rise — "I need Tanglin Rise's info now" has everything it needs.
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _capture_client("ok", calls))
    bubble.Api("pearl-vista").ask("i need to know Tanglin Rise's info now")
    ctx = "\n".join(m["content"] for m in calls[0]["messages"] if m["role"] == "system")
    assert "Tanglin Rise" in ctx and "Kranji" in ctx and "Pearl Vista" in ctx
    assert "400 kVA" in ctx and "rainscreen" in ctx          # records, not just titles
    assert "currently viewing: Pearl Vista" in ctx           # the default context


def test_conversation_survives_a_project_switch(monkeypatch):
    # Switching the dropdown must not amnesia the conversation.
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _capture_client("noted (D-001).", calls))
    bubble.Api("tanglin-rise").ask("why the non-combustible facade cladding?")
    bubble.Api("pearl-vista").ask("and does the older tower face the same facade issue?")
    roles = [(m["role"], m["content"]) for m in calls[1]["messages"]]
    assert any(r == "user" and "non-combustible facade" in c for r, c in roles)


def test_code_registry_reaches_the_llm_with_provisions_and_links(monkeypatch):
    # "Send me the clause" must be answerable without hunting: provisions and
    # official URLs are in the grounded context.
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _capture_client("ok", calls))
    bubble.Api().ask("show me the exact fire code clause")
    ctx = "\n".join(m["content"] for m in calls[0]["messages"] if m["role"] == "system")
    assert "CODE REGISTRY" in ctx
    assert "scdf.gov.sg" in ctx and "bca.gov.sg" in ctx      # both SG authorities' packs
    assert "non-combustible construction throughout" in ctx  # the provision itself


def test_court_records_are_part_of_the_llm_context(monkeypatch):
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _capture_client("ok", calls))
    bubble.Api("pearl-vista").ask("was the drone-only inspection proposal ever reviewed?")
    ctx = "\n".join(m["content"] for m in calls[0]["messages"] if m["role"] == "system")
    assert "COURT RECORD" in ctx and "Periodic Façade Inspection" in ctx


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
                        lambda **kw: _capture_client("Because SCDF Cl 3.5.1 (408213-D-001).", calls))
    out = json.loads(bubble.Api().ask("why the facde claddng??"))
    record = "\n".join(m["content"] for m in calls[0]["messages"] if m["role"] == "system")
    assert "408213-D-001" in record and "408213-D-002" in record   # full record in context
    assert "non-combustible mineral rainscreen" in record          # with rationale detail
    assert out["cited"] == ["408213-D-001"]                 # cited ids parsed from the answer


def test_conversation_history_is_passed_to_followups(monkeypatch):
    # A memory agent's chat must remember the conversation: the second call's
    # messages include the first question and answer.
    import openai
    calls = []
    monkeypatch.setattr(openai, "OpenAI",
                        lambda **kw: _capture_client("The record cites SCDF Cl 3.5.1 (408213-D-001).", calls))
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
                        lambda **kw: _fake_client("Locked (408213-D-001); the ACM swap (408213-D-002) was "
                                                  "rejected. (408213-D-999 and 517294-D-006 ignored)"))
    out = json.loads(bubble.Api().ask("why the facade cladding and can we change it"))
    # 408213-D-999 does not exist, and 517294-D-006 exists in NO project — the
    # project-coded id makes the filter a real cross-project hallucination check.
    assert out["cited"] == ["408213-D-001", "408213-D-002"]
    assert "408213-D-001" in out["answer"]
