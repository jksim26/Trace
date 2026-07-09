---
tags: [root]
---

# Trace

The design-decision memory agent for AEC. A *trace* is the unbroken line from
every design decision back to *why* it was made — Trace keeps that line
intact, and reasons along it: the moment a new decision breaks the premise an
older one stood on, it argues the case and records the verdict.

Where every other memory agent merely stores and retrieves, Trace **reasons
about decisions over time**.

## The three pillars

- [[Efficient Storage and Retrieval]]
- [[Timely Forgetting]]
- [[Recall Within Budget]]

## The modules

- [[Decision Store]] — the never-delete, bi-temporal foundation spine.
- [[Capture]] — Qwen function-calling reads a transcript, extracts decisions.
- [[Rule-pack (SCDF)]] — the deterministic compliance gate.
- [[Invalidation Alert]] — names the specific assumption a new decision breaks.
- [[Decision Court]] — three Qwen roles argue a gated conflict to a verdict.
- [[Hybrid Recall]] — lexical + semantic recall-to-budget, with abstention.
- [[MCP Tools]] — the four functions as Qwen-Agent custom tools.
- [[MCP Server]] — the deterministic, keyless MCP server over stdio.
- [[CLI Demo]] — the four-scene "Tanglin Rise" demo.
- [[Demo Scenarios]] — three projects, three companies, three code regimes.
- [[Ambient Trigger]] — one allowlist matcher, two worlds.
- [[Desktop Watcher]] — the real Windows foreground-window watcher.
- [[Workspace Demo]] — the browser-based simulated workspace.
- [[Ambient Bubble]] — the live local web app, one agent, one memory.

## Cross-cutting concepts

- [[Golden Thread]] — the SHA-256 hash-chained, tamper-evident audit log.
- [[Bi-temporal Time-Travel]] — `get_valid_asof` reconstructs what was known when.
