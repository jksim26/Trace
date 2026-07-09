---
tags: [module]
source: Trace/capture.py
---

# Capture

Qwen (`qwen-plus`) function-calling reads a meeting transcript and extracts
each decision with its rationale, assumptions, and author. Scene 1 of the
[[CLI Demo]].

## Related

- Writes to [[Decision Store]].
- Feeds [[Invalidation Alert]] once a decision lands.
- Exposed as a tool by [[MCP Tools]].
