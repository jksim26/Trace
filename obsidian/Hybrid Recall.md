---
tags: [module]
source: "Trace/recall.py, Trace/strategies.py, Trace/embeddings.py"
---

# Hybrid Recall

Blends lexical overlap with a Qwen text-embedding semantic signal, so a
paraphrase with no shared words ("make the exterior envelope cheaper" → the
facade decision) is still recalled. Packs only the valid critical decisions
within a token budget, cites them, and abstains honestly. Multi-strategy
ranking: relevance, recency, importance, composite, hybrid. The semantic half
degrades to the deterministic lexical path with no key. Scene 3 of the
[[CLI Demo]] (the token meter plus abstention).

## Related

- Reads valid decisions from [[Decision Store]].
- Powers [[Ambient Bubble]]'s chat.
- Implements [[Recall Within Budget]].
