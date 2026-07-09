---
tags: [pillar]
---

# Recalling critical memories within limited context windows

Track 1's third stated focus. Trace answers it with **retrieve-to-budget**
recall of only the currently-valid critical constraints, with honest
abstention, plus multi-strategy ranking (relevance, recency, importance,
composite).

## Implemented by

- [[Hybrid Recall]] — blends lexical overlap with a Qwen text-embedding
  semantic signal, packs only valid critical decisions within a token
  budget, cites them, abstains honestly.
- [[Ambient Bubble]] — the chat surface that consumes recall-to-budget.

## Related

- [[Trace]]
