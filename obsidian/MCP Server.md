---
tags: [module]
source: Trace/mcp_server.py
---

# MCP Server

The real MCP server (official `mcp` SDK, stdio) — eight deterministic,
keyless tools over the Model Context Protocol: the never-delete record
(`list_projects` / `list_decisions` / `get_decision`), bi-temporal
`decisions_asof`, the rule-pack gate `check_compliance` (returns the clause
plus official link), `get_code_provision`, `verify_audit_chain`, and the
persisted `court_records`. Any MCP client — Claude Desktop, a Qwen agent, an
IDE — can ground on Trace's *certain* half with no key and no network.

## Related

- Exposes [[Decision Store]], [[Golden Thread]], [[Bi-temporal Time-Travel]],
  [[Rule-pack (SCDF)]], and [[Decision Court]] records.
- Sibling of [[MCP Tools]].
- Implements [[Efficient Storage and Retrieval]].
