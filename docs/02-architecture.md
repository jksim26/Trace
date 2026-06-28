# 02 · Architecture & Framework — Keystone

*How it's built. Grounded in 2024–2026 memory-systems research (Graphiti, Letta/MemGPT, Mem0, Generative Agents) and the required Qwen Cloud stack.*
*Confidence tags: `[verified]` (primary paper/doc read) · `[web search]` · `[inference]`.*

---

## 1. Design principles (each maps to a Track-1 requirement)

1. **Decisions are first-class objects, not chat history.** A decision is a node carrying rationale + assumptions, not a buried message. → *"efficient memory storage"*
2. **Never delete — invalidate.** Superseded decisions are kept with a validity range and a `superseded_by` link. This is both the correct memory design *and* the golden-thread legal requirement. → *"timely forgetting of outdated information"* (forgetting = demoting the superseded from active recall, while preserving the trail)
3. **Active push, not passive pull.** Every new decision is checked against the graph on ingest; conflicts are pushed as alerts. This is the one thing no competitor does.
4. **Recall to a budget.** Retrieval ranks by relevance + recency + importance, filters to currently-valid, and packs only the top-k that fit a token budget. → *"recalling critical memories within limited context windows"*
5. **Deterministic where it matters.** The demo's centrepiece alert is gated on an explicit rule check, not pure LLM judgement, so it never misfires on stage. `[inference — risk mitigation]`
6. **Qwen-native.** Tools are exposed as MCP / custom skills via Qwen-Agent, to bank the judging hook directly.

---

## 2. The reference patterns we're standing on `[verified — papers read in research]`

| Pattern | Source | What we take from it |
|---|---|---|
| **Bi-temporal knowledge graph + edge invalidation** | Zep/**Graphiti** (arXiv 2501.13956) | The core data model. Each fact/edge carries *valid-time* (`valid_from`/`valid_to`, when true in the world) and *transaction-time* (`recorded_at`/`superseded_at`, when the system learned it). On a contradicting new edge, set the old edge's `valid_to = new.valid_from` and link `superseded_by` — **invalidate, never discard.** |
| **Always-in-context "core block" + paging** | **MemGPT/Letta** (arXiv 2310.08560) | A bounded working-memory block holding the live brief summary + currently-valid decisions + house rules; page the rest in on demand. |
| **Background "sleep-time" consolidation** | Letta | A separate pass that merges duplicates and refreshes the core-block summary during idle time (stretch goal). |
| **Composite recency + importance + relevance scoring** | **Generative Agents** (Park 2023) | Retrieval ranking signal: `score = relevance + recency + importance`, normalised. |
| **Extraction → Update with explicit ops** | **Mem0** (arXiv 2504.19413) | The ingest shape (extract candidate facts, then decide ADD/UPDATE/SUPERSEDE/NOOP). We replace Mem0's destructive DELETE with SUPERSEDE to keep the audit trail. |
| **Contextual hybrid retrieval** | **Anthropic Contextual Retrieval** (Sept 2024) | Prepend chunk-specific context before embedding + BM25; add rerank. Reported retrieval-failure cuts: 35% → 49% → 67%. |

**Why a graph at all, vs. flat vector memory:** flat fact stores (Mem0) and append-only streams (Generative Agents) cannot answer *"what did this decision assume, and what depends on it?"* — and Mem0's DELETE destroys the very history the golden thread requires. A bi-temporal decision graph is the only pattern that gives auditable, queryable supersession. `[inference, grounded in verified papers]`

---

## 3. Data model — the decision-dependency graph

### Node: `Decision`
```
Decision {
  id:            "D-047"
  statement:     "Facade = terracotta rainscreen on A2-s1,d0 mineral wool"
  discipline:    "architecture" | "structural" | "mep" | "fire" | "facade" | "cost" | "planning" | "client"
  riba_stage:    2                      # or AIA phase
  author:        ["R. Wells (arch)", "P. Desai (fire)"]
  rationale:     "HRB >18m; non-combustible cladding mandated by Approved Doc B (B4)."
  assumptions:   ["building remains an HRB (>18m)", "combustible cladding prohibited"]
  brief_ref:     "Facade specification / RDS-external-envelope"
  importance:    5                      # 1-5; deterministic by decision type, see §6
  # --- bi-temporal validity ---
  valid_from:    2026-01-14T11:42Z      # when true in the world
  valid_to:      null                   # null = currently valid
  recorded_at:   2026-01-14T11:45Z      # when the system learned it
  superseded_at: null
  status:        "valid" | "superseded" | "proposed"
  source_episode: "transcript-2026-01-14"
}
```

### Edge: dependency / supersession
```
(Decision)-[:ASSUMES]->(Premise)            # the premise an alert checks against
(Decision)-[:DEPENDS_ON]->(Decision)        # downstream blast-radius links
(Decision)-[:SUPERSEDED_BY]->(Decision)     # the immutable supersession chain
(Decision)-[:AFFECTS]->(BriefItem)          # the brief item it changes
```

### Storage choice for the hackathon `[inference — strong recommendation]`
**SQLite + a vector index, *not* Neo4j.** For a single project's decisions, graph traversal is a cheap BFS over a small table; SQLite is zero-ops and trivially packaged in an open-source repo. Cite Neo4j + Alibaba **DashVector** as the production path in the deck. Don't burn hackathon days standing up a graph DB.

The **three stores** (Graphiti-style subgraphs, simplified):
- **Episodic log** — append-only raw transcript chunks (provenance + re-extraction source).
- **Semantic decision graph** — the `Decision` nodes + edges above (the system of record).
- **Vector index** — embeddings of decision statements + rationale, for retrieval.

---

## 4. The two pipelines

### Pipeline A — Ingest & Invalidate (runs on every new transcript)
```
transcript chunk
   │
   ▼
[1] EXTRACT decisions          ── qwen3.7-max, function-calling → emits Decision record(s)
   │                              (statement, rationale, assumptions, author, discipline, brief_ref)
   ▼
[2] EMBED + LINK               ── text-embedding-v4 → vector index;
   │                              hybrid-search for semantically-related existing decisions
   ▼
[3] CONTRADICTION CHECK        ── for each related prior decision:
   │                              (a) RULE-PACK check (deterministic, §6) — does the new decision
   │                                  violate a known constraint a prior decision relied on?
   │                              (b) LLM premise check — does the new decision falsify a prior
   │                                  decision's stated assumption? (qwen3.7-max)
   │                              conflict = rule-hit OR high-confidence LLM-hit
   ▼
[4a] no conflict → ADD/UPDATE/NOOP        [4b] CONFLICT → fire INVALIDATION ALERT
   │                                          │  • name the prior decision + its rationale
   │                                          │  • explain why the new one breaks it
   ▼                                          │  • list downstream blast-radius (DEPENDS_ON BFS)
 commit Decision (valid)                      │  • offer: supersede (set prior.valid_to =
                                              │    new.valid_from, link superseded_by) — never delete
                                              ▼
                                          await human decision (human-in-the-loop)
```

### Pipeline B — Recall (runs on a query)
```
question ("why terracotta, and can we still change it?")
   │
   ▼
[1] embed query (text-embedding-v4, text_type=query)
   ▼
[2] HYBRID RETRIEVE  ── dense (cosine) + BM25 + graph BFS over related decisions
   ▼
[3] RERANK           ── qwen3-rerank (or gte-rerank-v2)
   ▼
[4] COMPOSITE RE-SCORE ── relevance + recency + importance; FILTER valid_to IS NULL
   │                       (default = currently-valid only; "audit mode" includes superseded)
   ▼
[5] RETRIEVE-TO-BUDGET ── greedily pack top-k decisions until token budget hit
   │                       (show a context-budget meter; this is the literal Track-1 ask)
   ▼
[6] ANSWER  ── qwen3.7-max, with citations to decision IDs;
              ABSTAIN ("no decision on record") if nothing valid is retrieved
```

---

## 5. The Qwen stack (full reference in [04-qwen-tech-reference.md](04-qwen-tech-reference.md))

| Component | Qwen Cloud / Model Studio choice | Why |
|---|---|---|
| Decision extraction (routine) | **qwen-plus** or **qwen-flash** | Cheap, 1M context; flash supports context caching for the stable brief prefix `[web search]` |
| Contradiction reasoning + final answers | **qwen3.7-max** (1M context, native iterative function-calling) | The hard reasoning; escalate only here to control cost `[web search]` |
| Embeddings | **text-embedding-v4** @ 1024-dim (Matryoshka; default, cost/quality sweet spot) | 8,192-token input, 100+ languages `[verified — Model Studio doc]` |
| Rerank | **qwen3-rerank** (or **gte-rerank-v2**) | After vector recall; hosted limits: ≤500 docs, 4,000 tok/item `[verified — doc]` |
| Agent framework / tools | **Qwen-Agent** (`QwenLM/Qwen-Agent`, install `[mcp]`) | Function-calling + **MCP client** + custom tools via `@register_tool` → banks the "custom skills / MCP" judging hook `[web search]` |
| API surface | OpenAI-compatible endpoint, **Singapore**: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | Reuse OpenAI SDK; Singapore is where the free quota lives `[verified — doc]` |

> **Avoid `qwen-long` (10M context).** It is Beijing-region-only and the Singapore free quota / $40 coupon likely won't cover it. We don't need 10M — the whole point of Keystone is *not* dumping everything into context. `[verified — region caveat; inference on need]`

> **Opt into the big window.** 1M-context models default to ~129K usable input unless you set `max_input_tokens`. Set it explicitly if you ever need it. `[web search]`

---

## 6. The rule-pack (demo reliability + AEC credibility)

The contradiction engine has two halves. The **LLM premise check** is general but probabilistic. To guarantee the demo never misfires, pair it with a small, explicit **AEC rule-pack** — deterministic constraints that, if violated, force the alert: `[inference — risk mitigation]`

```yaml
# rules/fire.yaml  (illustrative)
- id: ADB-B4-noncombustible
  applies_if: building.is_HRB == true        # >18m or >=7 storeys
  constraint: facade.cladding.rating in [A1, A2-s1d0]
  rationale: "Approved Document B prohibits combustible cladding over 18m"
  blast_radius: [structural.support, fire.cavity_barriers, partL.energy, gateway2.resubmit]
```

When a new decision (ACM cladding) violates a constraint a prior decision (D-047) relied on, the alert is **certain**. The rule-pack doubles as proof of AEC domain depth to judges. Keep it tiny — one or two rules covering the demo storyline; everything else falls through to the LLM check.

---

## 7. Memory taxonomy mapping (shows we understand memory systems) `[inference, grounded]`

| Memory type | In Keystone |
|---|---|
| **Working** (context window) | the bounded core block: live brief summary + currently-valid decisions + house rules |
| **Episodic** (events) | the append-only transcript log ("on 2026-03-03 the contractor proposed ACM") |
| **Semantic** (facts) | the decision graph — each decision is a fact with bi-temporal validity |
| **Procedural** (rules/skills) | the AEC rule-pack + the system prompt's house style |

**Forgetting policy:** decisions are *never* hard-deleted (audit trail). Decay/eviction applies only to **low-importance episodic chatter**, via composite-score demotion. Importance is **deterministic by decision type** (core/structural/fire decisions = 5; finish/FF&E choices = 2), not a free LLM rating — more predictable and defensible. `[inference]`

---

## 8. System diagram (text — turn into the required architecture diagram)

```
                        ┌─────────────────────────────────────────────┐
   meeting transcript ──▶                KEYSTONE AGENT                 │
   (or live chat)        │   (Qwen-Agent runtime, MCP tools)           │
                        │                                              │
                        │  MCP TOOLS / CUSTOM SKILLS:                  │
                        │   • capture_decision()                       │
                        │   • check_invalidation()                     │
                        │   • recall_decisions()                       │
                        │   • supersede_decision()                     │
                        └───────┬───────────────────────┬─────────────┘
                                │ extract / reason       │ embed / rank
                       qwen3.7-max / qwen-plus    text-embedding-v4 + qwen3-rerank
                                │                        │
        ┌───────────────────────┼────────────────────────┼───────────────────┐
        ▼                       ▼                        ▼                   ▼
  ┌───────────┐         ┌────────────────┐       ┌──────────────┐    ┌─────────────┐
  │ Episodic  │         │ Decision Graph │       │ Vector Index │    │  Rule-Pack  │
  │ log (raw) │         │  (bi-temporal) │       │ (embeddings) │    │ (AEC YAML)  │
  └───────────┘         └────────────────┘       └──────────────┘    └─────────────┘
        SQLite + vector index  (Neo4j + DashVector = production path)

  OUTPUTS:  ⚠ invalidation alert (push)   ·   answer + citations (pull)   ·   audit trail
```

---

## 9. Build order (so there's always a filmable thing)

1. Decision schema + SQLite store + never-delete supersession. *(spine)*
2. `capture_decision` via qwen3.7-max function-calling on one transcript. *(C1)*
3. `check_invalidation` = rule-pack + LLM premise check; push the alert. *(C2 — the centrepiece, do not cut)*
4. Hybrid retrieve + composite re-score + retrieve-to-budget + abstention + context-budget meter. *(C3)*
5. Audit/history view walking `superseded_by`. *(C4)*
6. Wrap 1–5 as **Qwen-Agent MCP tools**. *(C5)*
7. Thin UI/CLI to film the three scenes + architecture diagram + README + OSS license. *(C6)*

Stretch (only after the above is filmable): blast-radius graph visualisation; sleep-time consolidation; a LongMemEval-style eval harness scoring knowledge-update / temporal / abstention; the other three worked examples; a real graph DB.

---

*Next:* [03 · Hackathon Strategy →](03-hackathon-strategy.md)
