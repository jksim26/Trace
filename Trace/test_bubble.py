import json
from types import SimpleNamespace

import bubble


def _fake_client(answer="ok"):
    create = lambda **kw: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=answer))])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def test_state_returns_seeded_decisions():
    s = json.loads(bubble.Api().state())
    ids = [d["id"] for d in s["decisions"]]
    assert ids == ["D-001", "D-002"]
    assert s["decisions"][0]["status"] == "valid"
    assert s["decisions"][1]["status"] == "proposed"


def test_greeting_gets_a_pointer_not_an_abstention():
    # "hi" must not hit the decision store (nor the LLM — no monkeypatch needed:
    # if this path tried to build a client it would raise without a key).
    out = json.loads(bubble.Api().ask("hi"))
    assert "why the non-combustible facade" in out["answer"]
    assert out["cited"] == []
    out2 = json.loads(bubble.Api().ask("hello, testing?"))
    assert out2["cited"] == []
    assert "No decision on record" not in out2["answer"]


def test_real_question_still_reaches_recall(monkeypatch):
    import recall
    monkeypatch.setattr(recall, "OpenAI", lambda **kw: _fake_client("Because Cl 3.5.1 (D-001)."))
    out = json.loads(bubble.Api().ask("why the facade cladding"))
    assert out["cited"] == ["D-001", "D-002"]


def test_ask_cites_both_decisions(monkeypatch):
    import recall
    monkeypatch.setattr(recall, "OpenAI",
                        lambda **kw: _fake_client("Locked (D-001); the ACM swap (D-002) was rejected."))
    out = json.loads(bubble.Api().ask("why the facade cladding and can we change it"))
    assert out["cited"] == ["D-001", "D-002"]
    assert "D-001" in out["answer"]
