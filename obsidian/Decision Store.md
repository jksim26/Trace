---
tags: [module]
source: Trace/store.py
---

# Decision Store

The foundation spine: a never-delete, bi-temporal SQLite decision store.
Supersession closes `valid_to` and links `superseded_by` — never a `DELETE`.
Every write appends to the [[Golden Thread]]. Ships `get_valid_asof` for
[[Bi-temporal Time-Travel]].

## Feeds into

- [[Capture]] writes decisions here.
- [[Invalidation Alert]] reads prior decisions' assumptions from here.
- [[Decision Court]] persists verdicts back here.
- [[Hybrid Recall]] reads valid decisions from here.
- [[MCP Server]] and [[MCP Tools]] expose this store to agents.

## Implements

- [[Efficient Storage and Retrieval]]
