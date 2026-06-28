## SUMMARY
The 2024-2026 LLM agent memory landscape has converged on a few clear patterns. Frameworks split into two camps: (1) OS-inspired hierarchical/paged memory with agent-controlled tools (MemGPT/Letta), and (2) extract-and-store "memory layers" that distill conversations into discrete facts (Mem0) or temporal knowledge graphs (Zep/Graphiti, Cognee). A third research-driven camp emphasizes self-organizing memory (A-MEM's Zettelkasten linking) and the foundational Generative Agents memory stream (recency+importance+relevance scoring). For your Design Brief Memory Agent, the single most important finding is that bi-temporal knowledge graphs (Zep/Graphiti) are purpose-built for exactly the "obsolete decision" feature: facts are edges with both valid-time (t_valid/t_invalid — when true in the world) and transaction-time (t'_created/t'_expired — when the system learned it), and contradictions trigger edge invalidation rather than deletion, preserving a full audit trail of superseded decisions. [verified — I read the Zep paper arxiv 2501.13956]

On memory types, the field has standardized on a cognitive-science taxonomy: working memory (the context window), short-term (session buffer), and long-term split into episodic (events/experiences), semantic (facts/knowledge), and procedural (skills/rules/prompts). LangMem implements exactly this triad. Forgetting is now recognized as a feature, not a bug: unbounded "add-all" memory measurably degrades accuracy (one cited study: 13% accuracy with 2,400 records vs 39% with 248 curated records), so systems use time-decay (exponential or Weibull), access-frequency reinforcement (LRU/LFU), importance gating, consolidation/merge, and eviction. [web search — not independently verified]

Retrieval has converged on hybrid search: dense embeddings + BM25 + a cross-encoder reranker, with Anthropic's Sept-2024 Contextual Retrieval (prepending chunk-specific context before embedding/indexing) cutting retrieval failures 35% (embeddings), 49% (+BM25), and 67% (+rerank). Composite ranking that fuses semantic relevance with recency and importance (the Generative Agents formula) is widely reused. Context-window limits are handled via paging (MemGPT), recursive summarization/compaction on eviction, hierarchical core/recall/archival tiers, and retrieve-to-budget top-k selection. Evaluation centers on LoCoMo (long multi-session dialogues) and LongMemEval (500 questions across extraction, multi-session reasoning, temporal reasoning, knowledge-updates, and abstention) — the latter's knowledge-update and abstention categories map directly to your obsolete-decision use case.

My concrete recommendation: build a bi-temporal decision graph as the system-of-record (Graphiti-style edge invalidation for superseded decisions), wrap it with a Letta-style always-in-context "core block" holding the live brief summary, retrieve via contextual hybrid search + composite recency/importance/relevance scoring filtered to currently-valid facts, never hard-delete decisions (decay/archive instead), and run consolidation as a background "sleep-time" pass. Evaluate with a LongMemEval-style harness emphasizing knowledge-update and abstention.

## KEY FINDINGS
- **[high]** Zep/Graphiti uses a bi-temporal model with four explicit timestamp fields on every edge: t_valid and t_invalid (valid-time, when the fact was true in the world) and t'_created and t'_expired (transaction-time, when Zep ingested/expired it).
  - evidence: Paper defines Timeline T (chronological events) and Timeline T' (transactional ingestion); edge fields t'_created, t'_expired in T' and t_valid, t_invalid in T representing 'temporal range during which facts held true'.
  - source: https://arxiv.org/html/2501.13956v1
- **[high]** Graphiti's contradiction handling: an LLM compares each new edge against semantically related existing edges; on a temporally overlapping contradiction it INVALIDATES (not deletes) the old edge by setting its t_invalid to the t_valid of the new edge, consistently prioritizing new information.
  - evidence: Quoted: 'invalidates the affected edges by setting their t_invalid to the t_valid of the invalidating edge'; 'Graphiti consistently prioritizes new information'; outdated info is invalidated 'but not discard[ed]', preserving historical accuracy.
  - source: https://arxiv.org/html/2501.13956v1
- **[high]** Mem0's canonical paper uses a two-phase pipeline (Extraction then Update) where an LLM chooses one of four operations per candidate fact: ADD, UPDATE, DELETE (for facts contradicted by new info), or NOOP.
  - evidence: 'LLM determines which of four distinct operations to execute: ADD ... UPDATE ... DELETE for removal of memories contradicted by new information; and NOOP'. Note: a 2026 Mem0 blog separately describes an 'ADD-only single-pass' variant — I could not reconcile this discrepancy with the paper.
  - source: https://arxiv.org/html/2504.19413v1
- **[high]** Generative Agents (Park et al. 2023) retrieval score = recency + importance + relevance (all weights α=1); recency is exponential decay (γ=0.995 per hour) on last-access time, importance is an LLM-assigned 1-10 score at creation, relevance is cosine similarity; scores are min-max normalized to [0,1].
  - evidence: score = α_recency·recency + α_importance·importance + α_relevance·relevance with all α=1; decay factor reported as 0.995/hour (not 0.99); importance 1-10 LLM-rated; reflections periodically synthesize higher-level memories.
  - source: https://ar5iv.labs.arxiv.org/html/2304.03442
- **[high]** MemGPT/Letta treats the context window as RAM and external storage as disk, with three tiers: core memory (always in context, agent-editable blocks), recall memory (searchable conversation history), archival memory (long-term store); on overflow it evicts ~50% of the context and replaces it with a recursive summary.
  - evidence: Queue Manager flushes at a Flush Token Count, evicting oldest ~50% and replacing with a recursive summary; memory moves are exposed as agent tool calls (function calling).
  - source: https://arxiv.org/pdf/2310.08560
- **[medium]** Letta added 'sleep-time' agents: a separate background agent edits the primary agent's core memory blocks asynchronously during idle time; the primary agent cannot edit its own core memory in this architecture.
  - evidence: 'sleep-time agents handle memory management asynchronously'; memory-edit tools are attached to the sleep-time agent, which manages the primary agent's in-context memory blocks.
  - source: https://www.letta.com/blog/sleep-time-compute/
- **[high]** Anthropic's Contextual Retrieval (Sept 2024) prepends chunk-specific context before embedding/indexing, reducing retrieval failures by 35% (contextual embeddings), 49% (+contextual BM25), and up to 67% (+reranking).
  - evidence: Reported reductions: 35% / 49% / 67%; technique combines Contextual Embeddings + Contextual BM25 + rerank, with prompt caching to cut cost.
  - source: https://www.anthropic.com/news/contextual-retrieval
- **[medium]** Unbounded 'add-all' memory degrades agent accuracy; selective memory management outperforms it.
  - evidence: Cited study: add-all agents accumulated 2,400+ records and dropped to 13% accuracy, while selective agents kept 248 records at 39% accuracy.
  - source: https://hindsight.vectorize.io/blog/2026/05/21/agent-memory-consolidation
- **[high]** LangMem implements the cognitive triad — semantic (facts), episodic (past experiences/how problems were solved), procedural (learned behaviors/prompt rules) — via two modes: hot-path tools the agent calls inline and background managers that extract memories asynchronously, organized by namespaces.
  - evidence: LangMem docs/blog describe three memory types modeled on human memory plus hot-path vs background extraction and namespacing to prevent cross-contamination.
  - source: https://www.langchain.com/blog/langmem-sdk-launch
- **[high]** A-MEM applies the Zettelkasten method: each new memory becomes a structured note (contextual description, keywords, tags) plus an embedding; the system dynamically links related notes and triggers 'memory evolution' updates to existing notes' attributes when new memories arrive.
  - evidence: 'follows the basic principles of the Zettelkasten method'; notes carry attributes + embeddings; new memories can update existing notes' contextual representations.
  - source: https://arxiv.org/abs/2502.12110
- **[medium]** Cognee uses a modular ECL (Extract, Cognify, Load) pipeline that builds an ontology-validated knowledge graph plus vector embeddings, rather than plain chunk-and-embed RAG.
  - evidence: Extract (30+ connectors, OCR/AST chunking) -> Cognify (chunk, embed, entity/relationship extraction, ontology-based entity validation, coreference resolution) -> Load (writes vectors + graph edges).
  - source: https://github.com/topoteretes/cognee
- **[medium]** Zep reports DMR accuracy 94.8% (gpt-4-turbo) vs MemGPT 93.4%, and LongMemEval 71.2% (gpt-4o) vs a 60.2% full-context baseline with ~90% lower latency.
  - evidence: DMR: Zep 94.8%/98.2%, MemGPT 93.4%; LME gpt-4o: 71.2% at 2.58s vs baseline 60.2% at 28.9s; '18.5% accuracy improvement' with ~90% latency reduction.
  - source: https://arxiv.org/html/2501.13956v1
- **[high]** LoCoMo and LongMemEval are the dominant memory benchmarks; LongMemEval's five abilities (information extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention) directly cover the obsolete-decision/superseded-fact use case.
  - evidence: LoCoMo: ~10 dialogues, ~600 turns over up to 32 sessions, 1,540 QA (841 single-hop, 282 multi-hop, 321 temporal, 96 open-domain). LongMemEval: 500 questions across 6 categories incl. knowledge-update and abstention.
  - source: https://snap-research.github.io/locomo/
- **[low]** Mem0 reports strong LoCoMo/LongMemEval numbers but figures vary by source and version, so treat them as vendor-reported.
  - evidence: Original paper: ~26% higher accuracy than OpenAI memory, ~91% lower latency than full-context. 2026 Mem0 blog claims 92.5 LoCoMo / 94.4 LongMemEval at <7,000 tokens/retrieval. Numbers are self-reported.
  - source: https://mem0.ai/research

## STRUCTURED
## State of the Art: LLM Agent Memory Architectures (2024-2026)

All claims tagged by basis. [verified] = I read the primary source; [web search] = relayed from search snippets, not independently verified; [inference] = my synthesis.

---

### 1. Framework Comparison Table

| Framework | Core idea | Storage model | Retrieval | Contradiction / update handling | Strengths | Weaknesses |
|---|---|---|---|---|---|---|
| **MemGPT / Letta** | LLM-as-OS: context window = RAM, external store = disk; agent pages memory via tool calls | Tiered: **core** (always in-context, editable blocks), **recall** (conversation history), **archival** (long-term vector store) | Agent-issued search tools over recall/archival; explicit paging | Agent self-edits core blocks; **sleep-time agent** rewrites blocks in background; no automatic fact-level conflict resolution | Stateful, persistent, agent-controlled; mature runtime; good for long-running agents | Conflict handling is ad-hoc (LLM judgment, no formal temporal model); summarization can lose detail |
| **Mem0 / Mem0g** | Lightweight "memory layer" that distills chats into discrete facts | Vector store of fact strings (Mem0); **Mem0g** adds a graph of entities/relations | Multi-signal: dense + BM25 + entity matching, fused; time-aware ranking | **Extraction + Update** phases; LLM picks **ADD / UPDATE / DELETE / NOOP** per fact (DELETE for contradicted facts) | Token-efficient, low latency, production-focused, simple API | DELETE destroys history (no audit trail by default); fact-string store is flat; vendor-reported benchmarks |
| **Zep / Graphiti** | **Bi-temporal temporal knowledge graph** for agent memory | Three subgraphs: **episodic** (raw messages), **semantic entity** (extracted entities+relations as edges), **community** (clustered summaries); edges carry valid-time + transaction-time | `φ_cos` (cosine) + `φ_bm25` + `φ_bfs` (graph BFS), then rerankers (RRF, MMR, episode-mentions, cross-encoder LLM) | **Edge invalidation**: LLM detects contradiction vs related edges, sets old edge's `t_invalid = t_valid` of new edge; **invalidates, never deletes** | Best-in-class for evolving/obsolete facts; full audit trail; strong temporal reasoning | Heavier infra (graph DB); LLM extraction cost per ingest; complexity |
| **A-MEM** | Self-organizing memory via **Zettelkasten** linking | Notes = structured attributes (context, keywords, tags) + embeddings; dynamic inter-note links | Embedding similarity over notes + link traversal | **Memory evolution**: new notes can update attributes of linked existing notes | Emergent structure, no rigid schema; adaptive | Research-stage; no formal temporal/validity model; link explosion risk |
| **Cognee** | ETL-for-memory: **ECL** (Extract, Cognify, Load) building an ontology-grounded KG | Graph DB + vector DB; ontology/RDF-OWL validation, coreference resolution | GraphRAG-style: graph + vector hybrid | Ontology validation + coreference dedup; less explicit on temporal invalidation | Strong structured ingestion (30+ connectors); ontology grounding | Heavier setup; temporal-contradiction story weaker than Graphiti |
| **LangMem / LangGraph** | SDK exposing the cognitive memory triad over a pluggable BaseStore | Namespaced store; **semantic / episodic / procedural** memory types | Store search (vector); composable primitives | Hot-path tools + background managers extract/update; no built-in temporal graph | Clean abstractions, LangGraph integration, namespacing | Pre-1.0; conflict resolution left to the developer |
| **Generative Agents (Park 2023)** | Foundational **memory stream** with composite scoring + reflection | Append-only stream of natural-language observations + embeddings | **score = recency + importance + relevance** (α=1), min-max normalized; top-k to fit context | None formal — newer observations simply outrank older; reflections synthesize higher-level memories | Simple, influential, the origin of composite scoring | Append-only (no invalidation), unbounded growth, no dedup |

Sources: Letta/MemGPT [verified arxiv 2310.08560 + letta.com blogs]; Mem0 [verified arxiv 2504.19413v1]; Zep [verified arxiv 2501.13956v1]; A-MEM [web search arxiv 2502.12110]; Cognee [web search github/cognee.ai]; LangMem [web search langchain blog]; Generative Agents [verified ar5iv 2304.03442].

---

### 2. Memory Types in Agents

Two orthogonal axes have standardized across the literature [web search; well-corroborated]:

**By persistence / horizon:**
- **Working memory** = the live context window (the model's "RAM"; tokens currently attended to). [inference: this is the universal mapping]
- **Short-term memory** = the current session/conversation buffer (recent turns, scratchpad), often held in-context or in a rolling buffer.
- **Long-term memory** = persistent across sessions, stored externally (vector DB, graph, files) and retrieved on demand.

**By content type (cognitive taxonomy — LangMem implements all three explicitly):**
- **Episodic** — specific past events/experiences ("on 2026-03-04 the client rejected layout B"); answers *how* something happened.
- **Semantic** — durable facts/knowledge ("the brand primary color is #1A2B3C"); answers *what* is true.
- **Procedural** — learned behaviors/skills/rules, often baked into the system prompt or a "rules" block (e.g., "always present 3 concept options").

For a Design Brief agent, the mapping is clean [inference]: each **decision** is a semantic fact with validity (use the bi-temporal graph); the **stream of brief messages/revisions** is episodic; **house style/process rules** are procedural; the **active brief summary** lives in working memory (a core block).

---

### 3. Forgetting / Decay Mechanisms

Forgetting is now treated as a first-class feature; "remember everything" demonstrably hurts. [web search]

Consolidation policies operate on four levers (a useful framing from the Vectorize/Hindsight analysis) [web search — not verified]:
1. **Importance gating** — which observations become memories at all (Generative Agents: LLM rates 1-10 at creation; low-importance chatter never persists).
2. **Merge / consolidation** — related facts unified into one canonical record; periodic "reflection" (Generative Agents) or background "sleep-time" passes (Letta) synthesize higher-level memories.
3. **Decay** — confidence/retrieval-weight degrades over time. Two common forms:
   - Exponential recency decay (Generative Agents: γ=0.995 per hour on last-access time). [verified]
   - **Weibull-based decay** modeling relevance over time (Huang et al. 2025). [web search — not verified]
4. **Eviction** — memory leaves the system. Frequency-driven policies dominate: **MemOS uses LRU**, **XMem uses LFU**; access-frequency reinforcement keeps "hot" memories alive. [web search — not verified]

Empirical motivation [web search — single study, not verified]: an "add-all" agent reached 2,400+ records and 13% accuracy; a selectively-managed agent kept 248 records and hit 39%.

**Design implication for decisions:** do NOT hard-delete decisions (you need the obsolete-decision audit trail). Apply decay/eviction only to low-importance episodic chatter; decisions get *invalidated/archived*, not evicted. [inference]

---

### 4. DEEP DIVE — Temporal / Bi-Temporal Contradiction & Invalidation (central to "obsolete decision")

This is the most important section for your feature. The reference implementation is **Zep/Graphiti**, and the model is **bi-temporal**. [verified — read arxiv 2501.13956v1]

**Two independent timelines, four timestamps per edge (fact):**
- **Valid-time** (Timeline T): when the fact was *true in the real world*.
  - `t_valid` — when the fact started being true.
  - `t_invalid` — when it stopped being true (NULL = still valid).
- **Transaction-time** (Timeline T'): when the *system learned/recorded* it.
  - `t'_created` — when the edge was ingested.
  - `t'_expired` — when the system marked the edge superseded.

This separation is what lets you answer three distinct questions [inference, grounded in the paper]:
- "What is the current logo color?" → query edges where `t_invalid IS NULL`.
- "What did we believe the logo color was on March 1?" → query by transaction-time (`t'_created <= Mar1 < t'_expired`).
- "What was the logo color *as of* the Q1 brief?" → query by valid-time.

**The invalidation algorithm (verbatim mechanics):**
1. When a new edge is extracted, the system "employs an LLM to compare new edges against semantically related existing edges to identify potential contradictions." (It first narrows candidates by semantic similarity, so it does not compare against the whole graph.)
2. On a **temporally overlapping contradiction**, it "invalidates the affected edges by setting their `t_invalid` to the `t_valid` of the invalidating edge."
3. It "consistently prioritizes new information when determining edge invalidation."
4. Crucially: outdated info is "update[d] or invalidate[d], but not discard[ed]" — preserving historical accuracy "without large-scale recomputation."

**Why this beats the alternatives for obsolete decisions:**
- **Mem0's DELETE** removes the contradicted fact — you lose the history of *why* and *when* a decision changed. [verified — Mem0 paper lists DELETE for "memories contradicted by new information"]
- **Generative Agents / A-MEM** have no formal invalidation — a newer memory just outranks the old one, but the old one still surfaces and can mislead. [verified for Gen Agents]
- **Graphiti** gives you a queryable, auditable "this decision was superseded by that one on this date" trail — exactly the obsolete-decision UX.

**Pattern to adopt** [inference, modeled on Graphiti]: represent each design decision as a fact/edge with `valid_from`, `valid_to`, `recorded_at`, `superseded_at`, plus an explicit `supersedes`/`superseded_by` link to the decision that replaced it. Default retrieval returns only currently-valid decisions; an "audit/history" view walks the superseded chain.

---

### 5. Retrieval Ranking

Convergent best practice = **hybrid search + composite scoring + rerank**. [web search + verified components]

- **Hybrid lexical+dense:** dense embeddings (semantic) + BM25/Okapi (exact keyword) fused, then a **cross-encoder reranker** on the top candidates. Graphiti uses exactly this: `φ_cos` + `φ_bm25` + `φ_bfs`, then RRF / MMR / cross-encoder rerankers. [verified]
- **Contextual Retrieval (Anthropic, Sept 2024):** prepend an LLM-generated chunk-specific context blurb before embedding AND before BM25 indexing. Failure-rate reductions: **35%** (contextual embeddings), **49%** (+contextual BM25), **67%** (+reranking). Pair with prompt caching to control cost. [verified — anthropic.com/news/contextual-retrieval]
- **Composite recency/importance/relevance:** the Generative Agents formula `score = recency + importance + relevance` (normalized) is widely reused to bias retrieval toward fresh, significant, on-topic memories. Mem0 similarly fuses relevance + importance + recency. [verified for Gen Agents; web search for Mem0]
- **Graph-traversal retrieval:** start from semantically matched nodes, then BFS to pull related/connected facts (GraphRAG, Graphiti `φ_bfs`, Cognee). Good for "show me all decisions related to the hero section." [verified for Graphiti]

**Note:** your existing `wiki-retrieve` skill already implements the contextual-prefix + BM25 + cosine-rerank pattern — that is the same Anthropic approach and a sensible primitive to reuse. [verified — from the skill description in this environment]

---

### 6. Handling Limited Context Windows

Techniques, roughly in order of how aggressively they reclaim space [web search + verified]:
- **Hierarchical tiers + paging (MemGPT):** keep a small always-in-context **core block**; page recall/archival in on demand via tool calls.
- **Recursive summarization / compaction on eviction:** when the buffer hits a flush threshold, evict ~50% of oldest turns and replace with a recursive summary (MemGPT Queue Manager). [verified arxiv 2310.08560]
- **Retrieve-to-budget:** rank candidate memories (composite score), then greedily include top-k until the token budget is hit (Generative Agents: "top-ranked memories that fit within the context window"). This is the literal mechanism behind the Track-1 phrasing "recalling critical memories within limited context." [verified]
- **Background/sleep-time consolidation (Letta):** a separate agent reorganizes and compresses memory during idle time, so the live context stays lean without blocking responses. [web search]
- **Core-block summary maintenance:** keep a continuously-updated, bounded summary of the active brief in-context (semantic compression of the whole project state). [inference]

---

### 7. Evaluation

- **LoCoMo** (Snap): very long multi-session dialogues — ~10 conversations, ~600 turns over up to 32 sessions; **1,540 QA** split into 841 single-hop, 282 multi-hop, 321 temporal-reasoning, 96 open-domain. Widely used but criticized for size/leakage; treat leaderboard scores cautiously. [web search — snap-research.github.io/locomo]
- **LongMemEval:** **500 questions** testing five abilities — information extraction, multi-session reasoning, **temporal reasoning**, **knowledge updates**, and **abstention** — embedded in long synthetic histories; six question categories incl. single-session user/assistant/preference recall, knowledge-update, temporal, multi-session. The **knowledge-update** and **abstention** categories are the closest existing analog to your obsolete-decision feature. [web search — not independently verified]
- **DMR (Deep Memory Retrieval):** older, near-saturated; Zep 94.8-98.2%, MemGPT 93.4%. [verified, but vendor-reported]
- Newer harnesses (MemoryAgentBench, AMA-Bench, BEAM, MemoryCD) explicitly add **selective forgetting** and **cross-domain personalization** dimensions. [web search — names only, not verified]

**Recommendation:** build a small LongMemEval-style harness over real design-brief histories that specifically scores (a) retrieving the *current* decision when one was superseded, (b) correctly citing the *prior* decision on a historical query, and (c) **abstaining** when no decision exists. Track contradiction-detection precision/recall separately. [inference]

---

### 8. Recommended Architecture for the Design Brief Memory Agent

A hybrid that takes the best of Graphiti (temporal correctness) and Letta (in-context working memory + background consolidation): [inference, grounded in the verified sources above]

1. **System-of-record = bi-temporal decision graph (Graphiti pattern).**
   - Each decision is a fact/edge: `{subject, predicate, object, valid_from, valid_to, recorded_at, superseded_at, supersedes/superseded_by, importance, source_episode}`.
   - On every new brief input: LLM extracts candidate decision facts → hybrid-search for semantically related existing decisions → LLM contradiction check → if contradicted, set old `valid_to = new.valid_from`, set `superseded_at`, link `superseded_by`. **Never delete.**

2. **Working memory = a Letta-style always-in-context "core block"** holding the live brief summary + active (currently-valid) decisions + house-style rules (procedural). Bounded; maintained by compaction.

3. **Episodic log** = append-only raw brief messages/revisions (cheap store), used for provenance and re-extraction.

4. **Retrieval = contextual hybrid (your `wiki-retrieve`) → composite re-score.**
   - Contextual embeddings + BM25 + cross-encoder rerank.
   - Re-rank with `relevance + recency + importance`, and **filter to `valid_to IS NULL` by default** (currently-true decisions); expose an explicit "history/audit" mode that includes superseded edges.
   - Graph BFS to pull related decisions for a topic.

5. **Forgetting = decay + archive, not delete.** Decay importance of stale episodic chatter and evict low-value observations (LRU/LFU); decisions are only ever invalidated/archived (audit trail intact).

6. **Consolidation = background "sleep-time" pass** that merges duplicate facts, refreshes the core-block summary, and synthesizes higher-level "themes" (reflection).

7. **Context budgeting = retrieve-to-budget top-k** with recursive summarization fallback for the episodic log.

8. **Evaluation = LongMemEval-style harness** weighted toward knowledge-update, temporal, and abstention; plus a contradiction-detection precision/recall metric.

This directly satisfies the "obsolete decision" requirement (bi-temporal edge invalidation) and the Track-1 "recall critical memories within limited context" requirement (composite-scored retrieve-to-budget over a bounded core block).

## OPEN QUESTIONS
- Mem0 discrepancy: the canonical 2025 paper specifies ADD/UPDATE/DELETE/NOOP, but a 2026 Mem0 blog describes an 'ADD-only single-pass' design. Unclear whether this is a newer version, a different product tier, or imprecise marketing — needs verification against current source/release notes before relying on it.
- All benchmark numbers (Mem0, Zep DMR/LongMemEval, ByteRover LoCoMo 92.2%) are vendor- or paper-reported and not independently reproduced; LoCoMo in particular has documented criticisms (small size, potential leakage). Independent replication needed before treating any leaderboard ranking as decisive.
- Whether to store the decision graph in a real graph DB (Neo4j, as Graphiti uses) vs a lightweight bi-temporal schema over SQLite/files — depends on expected scale and whether graph traversal queries are actually needed for the brief use case.
- Exact Graphiti behavior when valid-time of a contradiction is unknown/unspecified (does it fall back to transaction-time?) — the paper describes the overlapping-valid-time case; the missing-timestamp case was not confirmed in the sources I read.
- How importance is best scored for design decisions specifically (LLM 1-10 rating vs explicit user flags vs decision type) — Generative Agents uses LLM rating, but a brief agent may want deterministic importance from decision category.

## SOURCES
- https://arxiv.org/html/2501.13956v1
- https://arxiv.org/abs/2501.13956
- https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/
- https://help.getzep.com/graphiti/getting-started/overview
- https://arxiv.org/pdf/2310.08560
- https://www.letta.com/blog/letta-v1-agent
- https://www.letta.com/blog/sleep-time-compute/
- https://www.letta.com/blog/memory-blocks/
- https://arxiv.org/html/2504.19413v1
- https://arxiv.org/abs/2504.19413
- https://mem0.ai/research
- https://mem0.ai/blog/state-of-ai-agent-memory-2026
- https://mem0.ai/blog/memory-eviction-and-forgetting-in-ai-agents
- https://arxiv.org/abs/2502.12110
- https://github.com/topoteretes/cognee
- https://www.cognee.ai/blog/deep-dives/grounding-ai-memory
- https://www.langchain.com/blog/langmem-sdk-launch
- https://ar5iv.labs.arxiv.org/html/2304.03442
- https://arxiv.org/abs/2304.03442
- https://www.anthropic.com/news/contextual-retrieval
- https://snap-research.github.io/locomo/
- https://hindsight.vectorize.io/blog/2026/05/21/agent-memory-consolidation
- https://arxiv.org/html/2603.07670v1