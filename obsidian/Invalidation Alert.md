---
tags: [module]
source: Trace/invalidate.py
---

# Invalidation Alert

The centrepiece: premise-aware. It names the *specific stored assumption* a
new decision breaks, gated by [[Rule-pack (SCDF)]] where the rule-pack
applies, and falling back to an LLM premise check that reads each prior
decision's assumptions when the rule-pack is silent. Scene 2 of the
[[CLI Demo]] (the red alert).

Now takes each project's own building context explicitly (rather than one
hardcoded building shared by every project — a real bug this update fixed,
see [[Demo Scenarios]]), so a 95 m tower's height rules can't fire on a
two-storey shed.

## Related

- Reads assumptions from [[Decision Store]].
- Gated by [[Rule-pack (SCDF)]].
- Triggers [[Decision Court]], which now treats a rule hit (deterministic
  REJECT) differently from an LLM-premise hit (the Judge genuinely decides).
- Implements [[Timely Forgetting]].
