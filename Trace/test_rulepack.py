from rulepack import load_rules, check, Rule


def test_load_rules_includes_scdf_rule():
    ids = [r.id for r in load_rules()]
    assert "SCDF-Cl3.5-noncombustible" in ids


def test_combustible_cladding_over_15m_violates():
    context = {"building": {"height_m": 95}, "facade": {"cladding": {"combustible": True}}}
    violations = check(context, load_rules())
    assert [v.rule_id for v in violations] == ["SCDF-Cl3.5-noncombustible"]
    assert "15 m" in violations[0].rationale
    assert "SCDF" in violations[0].citation
    assert any("s.9" in b for b in violations[0].blast_radius)


def test_noncombustible_cladding_over_15m_ok():
    context = {"building": {"height_m": 95}, "facade": {"cladding": {"combustible": False}}}
    assert check(context, load_rules()) == []


def test_rule_does_not_apply_below_15m():
    context = {"building": {"height_m": 10}, "facade": {"cladding": {"combustible": True}}}
    assert check(context, load_rules()) == []


def test_operators_via_inline_rule():
    rules = [Rule(id="r", when={"a": {"gte": 5}}, require={"b": {"in": ["x", "y"]}})]
    assert check({"a": 5, "b": "z"}, rules)[0].rule_id == "r"   # applies, require fails
    assert check({"a": 5, "b": "x"}, rules) == []               # require satisfied
    assert check({"a": 4, "b": "z"}, rules) == []               # does not apply


def test_missing_require_field_does_not_violate():
    # The require attribute is absent (the decision doesn't set cladding at all),
    # so the rule must NOT fire — only a present-and-combustible value does.
    assert check({"building": {"height_m": 95}}, load_rules()) == []
