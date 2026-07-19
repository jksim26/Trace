---
tags: [module]
source: "Trace/scenarios.py, Trace/rules/sg-bca/"
---

# Demo Scenarios

Three demo projects, three companies, three code **stories** — all
Singapore now: **tanglin-rise** (SG residential high-rise, SCDF fire
rule-gated), **kranji-hub** (SG industrial/MEP, the LLM-premise-check
story, no rule involved), **pearl-vista** (a 78 m residential tower past
its 20th year, gated by a *different* Singapore authority's rule-pack —
the BCA Periodic Façade Inspection regime). Pearl Vista replaced the old
UK-based "Maple Wharf" scenario, re-anchoring the whole pitch on the
Singapore Qualified Person personal/criminal liability angle rather than
splitting it across two jurisdictions. Each store carries valid decisions,
rejected proposals, superseded chains, and court records — real memory to
recall.

Each project also now carries its own building context (height, boundary
distance, etc.) passed explicitly into [[Invalidation Alert]] — a real bug
this update fixed: every project's compliance check used to run against
Tanglin Rise's hardcoded 95 m building, silently wrong for Kranji Hub and
Pearl Vista.

## Related

- Populates [[Decision Store]] with project-coded ids.
- Consumed by [[CLI Demo]] and [[Ambient Bubble]]'s project switcher.
- Pearl Vista uses a different [[Rule-pack (SCDF)]] (BCA, not SCDF).
- Also exported into the [[Knowledge Base Vault]] and watched by
  [[Vault Watcher]], one `kb/<project>/` folder per project.
