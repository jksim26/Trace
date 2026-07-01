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


def test_ask_cites_both_decisions(monkeypatch):
    import recall
    monkeypatch.setattr(recall, "OpenAI",
                        lambda **kw: _fake_client("Locked (D-001); the ACM swap (D-002) was rejected."))
    out = json.loads(bubble.Api().ask("why the facade cladding and can we change it"))
    assert out["cited"] == ["D-001", "D-002"]
    assert "D-001" in out["answer"]
