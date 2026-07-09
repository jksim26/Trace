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

## Related

- Reads assumptions from [[Decision Store]].
- Gated by [[Rule-pack (SCDF)]].
- Triggers [[Decision Court]].
- Implements [[Timely Forgetting]].
