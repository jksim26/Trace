---
tags: [module]
source: Trace/store.py
---

# Decision Store

The foundation spine: a never-delete, bi-temporal SQLite decision store.
Supersession closes `valid_to` and links `superseded_by` — never a `DELETE`.
Every write appends to the [[Golden Thread]]. Ships `get_valid_asof` for
[[Bi-temporal Time-Travel]].

**Decision ids are now project-coded**: each project has its own six-digit
code (stored in a new `meta` table, set once before a store's first write),
and ids are minted as `<code>-D-<nnn>` instead of a plain `D-001` that
repeated across every project — an id now names its own project wherever
it's cited, across the bubble's chat, MCP clients, and court records.

A new `episodes` table stores the raw source note or transcript a decision
was extracted from, append-only and content-addressed (dedupe by hash, not
by filename) — provenance is now a real, readable record, not just a label.

## Feeds into

- [[Capture]] writes decisions here.
- [[Invalidation Alert]] reads prior decisions' assumptions from here.
- [[Decision Court]] persists verdicts back here, and now directly adopts,
  rejects, and supersedes decisions here too.
- [[Hybrid Recall]] reads valid decisions from here.
- [[MCP Server]] and [[MCP Tools]] expose this store to agents.
- [[Knowledge Base Vault]] renders the whole store out as a markdown vault.
- [[Vault Watcher]] writes new episodes and decisions in here on ingest.

## Implements

- [[Efficient Storage and Retrieval]]
