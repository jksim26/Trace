---
tags: [concept]
---

# Golden thread

Every write to the [[Decision Store]] appends to a SHA-256 hash-chained audit
log. `verify_audit_chain()` recomputes the chain and detects any alteration —
a tamper-evident record of *why*, the "golden thread" the UK Building Safety
Act makes legally mandatory, and the defence a personally and criminally
liable engineer has otherwise never had.

## Related

- [[Decision Store]]
- [[MCP Server]] — exposes `verify_audit_chain` as a tool.
- [[Efficient Storage and Retrieval]]
