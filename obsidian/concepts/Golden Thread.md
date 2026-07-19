---
tags: [concept]
---

# Golden thread

Every write to the [[Decision Store]] appends to a SHA-256 hash-chained audit
log. `verify_audit_chain()` recomputes the chain and detects any alteration —
a tamper-evident record of *why*, the "golden thread" the UK Building Safety
Act makes legally mandatory, and the defence a personally and criminally
liable engineer has otherwise never had.

The same guarantee now extends one layer further, to the [[Knowledge Base
Vault]]'s markdown projections: each generated note carries a
`record_sha256` of its underlying row, and `verify_vault()` re-renders the
expected note and diffs it against what's on disk — the vault-level
analogue of `verify_audit_chain`, catching an edited projection the same
way the chain catches an altered log entry.

## Related

- [[Decision Store]]
- [[MCP Server]] — exposes `verify_audit_chain` as a tool.
- [[Knowledge Base Vault]] — `verify_vault()`, the markdown-level analogue.
- [[Efficient Storage and Retrieval]]
