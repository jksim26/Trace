# Temporal Reasoning Engine — Phase 1 Design Spec

*2026-07-01. Locked in brainstorming. Goal: move Trace from "store + retrieve" (every memory agent) to a **temporal reasoning engine for decisions** — the substance that lifts the Technical (30%) and Innovation (30%) scores, and the "why Trace beats a chat agent" story.*

## What we're building (Phase 1, in order)

1. **Bi-temporal time-travel recall** — query the decision state *as of any past date*. We already have the bi-temporal columns (`valid_from/valid_to/recorded_at/superseded_at`); this exposes them. *"What did we believe was valid on 3 March?"* Near-free, high-wow, unique.
   - Interface: `store.get_valid_asof(conn, as_of) -> list[Decision]` — decisions recorded and valid in world-time as of `as_of`.
2. **Multi-strategy recall** — recall visibly orchestrates several strategies: **relevance** (semantic), **recency**, **importance** (criticality), **dependency** (graph — what rests on this), **validity** (time-travel). The direct MemoryAgent showcase.
3. **Core / domain split** — separate the domain-agnostic engine (store, capture, invalidate, recall) from a pluggable **AEC domain pack** (the codebook, disciplines, the rule-pack). Makes "niche now, broaden later via a domain pack" a real architecture, and is itself a depth point.
4. **The decision court (A)** — multi-agent adversarial invalidation: Proposer / Guardian (cites the clause + the conflicting decision) / Judge (verdict + written rationale). The innovation showpiece and the video's centrepiece; reuses the rule-pack (as the Guardian's evidence) and the Qwen-Agent/MCP setup.

## Out of scope (roadmap — narrate, don't build)
Cascade graph (B), eval harness, the hands-free ingestion connectors, on-prem shell. These are the pitch/roadmap.

## Approach
- Each piece is TDD, additive, and independently demoable — never big-bang; the current working demo stays the fallback at every step.
- The CLI/bubble gain a **time-travel beat** and a **court beat** for the video.
- Positioning: **ruthlessly niche AEC** in the pitch; domain-agnostic *core* under the hood.

## Success criteria
- `get_valid_asof` returns the correct historical state across a supersession (tested).
- Recall exposes ≥3 named strategies.
- The rule-pack + codebook live behind a domain-pack boundary the engine imports.
- The court returns a structured verdict (for/against/rationale) on the Tanglin Rise conflict.
