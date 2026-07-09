---
tags: [pillar]
---

# Efficient storage and retrieval

Track 1's first stated focus. Trace answers it with a **bi-temporal decision
store**: decisions as first-class records carrying rationale and assumptions,
with never-delete supersession, plus time-travel recall.

## Implemented by

- [[Decision Store]] — `get_valid_asof` reconstructs what was valid *and
  known* as of any date.
- [[Bi-temporal Time-Travel]]
- [[MCP Server]] — exposes the store's read paths with no key, no network.

## Related

- [[Trace]]
