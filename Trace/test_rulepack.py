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


def test_boundary_limb_fires_below_15m_when_within_1m_of_boundary():
    # Cl 3.5.1's OTHER limb: within 1 m of the boundary, non-combustible is
    # mandated regardless of height.
    context = {"building": {"height_m": 10, "boundary_distance_m": 0.5},
               "facade": {"cladding": {"combustible": True}}}
    assert [v.rule_id for v in check(context, load_rules())] == ["SCDF-Cl3.5.1-boundary"]


def test_lowrise_class0_limb():
    # Cl 3.5.4: below 15 m and 1 m+ from the boundary, cladding must still be
    # Class 0 / EN 13501-1 Class B.
    context = {"building": {"height_m": 12, "boundary_distance_m": 5},
               "facade": {"cladding": {"class_0": False}}}
    assert [v.rule_id for v in check(context, load_rules())] == ["SCDF-Cl3.5.4-lowrise-class0"]


def test_acp_core_limb():
    # Cl 3.15.13: a composite panel whose core is not Class 0 / Class B fails,
    # independent of height (the Toh Guan Road failure mode).
    context = {"facade": {"cladding": {"is_composite": True, "core_class0_or_b": False}}}
    assert [v.rule_id for v in check(context, load_rules())] == ["SCDF-Cl3.15.13-acp-core"]


def test_every_rule_carries_its_provision_and_official_source():
    # Automation, not a tool: the clause comes to the user with its link —
    # nobody gets sent off to search a statutes portal.
    for r in load_rules():
        assert r.provision, r.id
        assert r.url.startswith("https://"), r.id


def test_uk_pack_loads_separately_and_fires_over_18m():
    # A different jurisdiction is a different rule-pack, same engine.
    import rulepack
    from pathlib import Path
    uk = load_rules(Path(rulepack.__file__).with_name("rules") / "uk")
    context = {"building": {"height_m": 62}, "facade": {"cladding": {"combustible": True}}}
    assert [v.rule_id for v in check(context, uk)] == ["UK-Reg7-2-combustible-ban"]
    assert check({"building": {"height_m": 16}, "facade": {"cladding": {"combustible": True}}}, uk) == []


def test_uk_pack_is_not_loaded_by_default():
    # The default (Singapore) pack must not pick up subdirectory packs, or the
    # demo's one-rule invariant breaks.
    assert all(not r.id.startswith("UK-") for r in load_rules())


def test_demo_context_still_fires_exactly_one_rule():
    # The Tanglin Rise demo context (95 m, 7.5 m boundary) must trip only the
    # height limb — the centrepiece alert stays deterministic and single.
    context = {"building": {"height_m": 95, "boundary_distance_m": 7.5},
               "facade": {"cladding": {"combustible": True}}}
    assert [v.rule_id for v in check(context, load_rules())] == ["SCDF-Cl3.5-noncombustible"]
