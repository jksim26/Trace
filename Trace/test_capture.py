import json
from types import SimpleNamespace

from capture import parse_tool_calls


def _fake_tc(args: dict):
    return SimpleNamespace(function=SimpleNamespace(name="record_decision", arguments=json.dumps(args)))


def test_parse_maps_fields_and_attributes():
    tcs = [_fake_tc({
        "statement": "Facade = non-combustible mineral rainscreen",
        "discipline": "facade",
        "rationale": "SCDF Cl 3.5 requires non-combustible external wall over 15 m",
        "assumptions": ["building exceeds 15 m"],
        "author": ["K. Lim"],
        "cladding_combustible": False,
    })]
    captured = parse_tool_calls(tcs, source_episode="t01")
    assert len(captured) == 1
    c = captured[0]
    assert c.decision.discipline == "facade"
    assert c.decision.assumptions == ["building exceeds 15 m"]
    assert c.decision.author == ["K. Lim"]
    assert c.decision.source_episode == "t01"
    assert c.attributes == {"cladding_combustible": False}


def test_parse_omits_null_cladding_attribute():
    tcs = [_fake_tc({
        "statement": "Core moved 2 m east",
        "discipline": "architecture",
        "rationale": "improves floorplate efficiency",
        "assumptions": [],
        "author": ["K. Lim"],
        "cladding_combustible": None,
    })]
    assert parse_tool_calls(tcs)[0].attributes == {}


def test_parse_handles_no_calls():
    assert parse_tool_calls(None) == []
    assert parse_tool_calls([]) == []
