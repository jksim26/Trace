---
tags: [module]
source: Trace/mcp_tools.py
---

# MCP Tools

The four core functions — capture, invalidate, court, recall — exposed as
Qwen-Agent custom tools (LLM-driven), so a Qwen Assistant calls them itself
autonomously (e.g. `capture_decision` then `check_invalidation` concluding
the PE-core ACP swap invalidates D-001).

## Related

- Wraps [[Capture]], [[Invalidation Alert]], [[Decision Court]], [[Hybrid Recall]].
- Sibling of [[MCP Server]] (that one is deterministic/keyless; this one is
  LLM-driven).
