---
tags: [module]
source: "Trace/rulepack.py, Trace/rules/fire.yaml, Trace/rules/sg-bca/facade.yaml"
---

# Rule-pack (SCDF)

The deterministic rule-pack — four rules from the primary-source research
(Cl 3.5.1 height and boundary limbs, Cl 3.5.4 low-rise Class 0, Cl 3.15.13
ACP core): the gate that keeps the [[Invalidation Alert]] reliable on
camera.

Note despite the note's title, this is no longer UK-vs-Singapore: the
old UK pluggable pack (regulation 7(2)) was retired when the whole demo
went all-Singapore. Pearl Vista now swaps in a *different* Singapore
authority's pack instead — `rules/sg-bca/facade.yaml`, the BCA Periodic
Façade Inspection regime — proving rule-packs are pluggable per code
*authority*, not just per country. See [[Demo Scenarios]].

Each project now passes its own building context (height, boundary
distance) into the check, instead of one hardcoded building shared by
every project — see the bugfix note on [[Demo Scenarios]].

## Related

- Gates [[Invalidation Alert]].
- Gates conflicts that reach the [[Decision Court]] (only rule hits force
  a deterministic REJECT; LLM-premise alerts let the Judge decide).
- Exposed via `check_compliance` in [[MCP Server]].
- Implements [[Timely Forgetting]].
