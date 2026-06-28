# 05 · Competitive Landscape — Why We Win the Room

*All "does NOT" entries are `[inference]` from product positioning + the absence of any contrary claim — not vendor disclaimers. To harden before a judge, a hands-on check of one AEC tool (Revizto/ACC) and one second-brain (Supermemory) would confirm no hidden invalidation feature.*

---

## 1. The landscape splits into two camps — neither closes the loop

**Camp A — AEC tools** are excellent at geometric clash detection, spatially-anchored issues, and audit trails, but they track **what is wrong in the model**, not **why a choice was made** or **whether a past choice still holds.**

**Camp B — horizontal AI memory / KB tools** increasingly do typed "decisions" memory and even generic contradiction detection, but **none target AEC**, understand disciplines/systems/model elements, or model **design-decision dependencies.**

The closest *conceptual* analogue isn't in AEC at all — it's the software **Architecture Decision Record (ADR)**: decision + rationale + superseded-by link. But ADR supersession is a **manual** human status flip, software-only, with **no automatic detection.**

---

## 2. Competitor table

| Tool | Category | Does | Does **NOT** do |
|---|---|---|---|
| **Revizto** | AEC clash + issue tracking | Real-time clash detection, auto issue creation, spatially-anchored issues, full audit trail | Capture *why* a choice was made; detect that a new decision invalidates an earlier one |
| **Newforma Konekt** (ex-BIM Track) | AEC coordination/PM | Issue tracking in Revit/Navisworks, "golden thread" project info | Per-decision rationale/assumptions; decision-dependency graph; active invalidation alerts |
| **BIMcollab** | OpenBIM issue mgmt (BCF) | BCF issues, rule-based model checking, clash detection | Stores comments+screenshots on elements, not decision rationale; no temporal invalidation |
| **Autodesk Construction Cloud / BIM 360** | CDE + issues/RFIs | Clash→issue conversion, Issue↔RFI linking, traceable workflow status | Reasoning behind decisions; engine to detect a superseded/invalidated *decision* |
| **Oracle Aconex** | Document control / CDE | Versioned docs, structured RFI/submittal mail, full audit trails | Decision-rationale graph; downstream-decision invalidation |
| **Asite / Procore** | CDE / construction PM | Document control, version control, RFIs/submittals, field access | Rationale capture; decision-dependency or invalidation engine |
| **Helonic** (ex-Articulate, YC) | AI drawing review / RFI-gen | AI reviews 2D PDF sets for coordination conflicts, code compliance, missing info; pushes RFIs | Track decisions *over time*, their rationale, or detect a later decision invalidating an earlier one (forward, point-in-time) |
| **Drawer AI / Togal.AI / Bynaus** | AI drawing analysis / takeoff / field docs | Change analysis, VE reports, takeoff, structured field records | Decision-rationale memory; semantic decision-conflict detection |
| **Knowledge Architecture (Synthesis) / Workorb** | AEC knowledge mgmt | AEC intranet + AI search (RAG) over firm content; proposal knowledge graph | Per-project design decisions, rationale, or invalidation (retrieval, not a dependency engine) |
| **ADRs** (adr-tools) | SW decision records | decision + context + rationale + **superseded** link | **Manual** supersession; software-only; **no automatic invalidation detection** |
| **Decision logs** (monday/Loqbooq/Jira) | Generic PM log | Manual what/who/when/why; some construction use | Static manual tables; no dependency graph; no invalidation; not AEC-aware |
| **Supermemory / Second Brain / Mem0 / Zep** | Horizontal AI memory | Persistent memory, RAG, typed "decisions", generic contradiction/update handling | No AEC domain model; no design-decision dependency graph; contradiction is fact-level, not downstream-decision invalidation |
| **Alhena / Fini** | AI KB contradiction detection | Auto-flag contradictory FAQ/support articles | Operate on FAQ text, not a graph of design decisions + assumptions; no AEC; no downstream invalidation |

---

## 3. The unoccupied square

The capability we need is **split across four groups, owned whole by none:**

- **AEC issue/CDE tools** → have timestamp + audit, but track issues/clashes/docs, no rationale, no dependency model.
- **ADRs** → have rationale + supersede-link, but manual, software-only, no auto-detection.
- **Horizontal AI memory** → has typed decisions + generic contradiction handling, but no AEC model, no dependency graph.
- **Decision logs** → capture who/when/why, but static manual tables, no invalidation engine.

> **The empty square Keystone fills:** an AEC-aware system where decisions are first-class nodes carrying **rationale + assumptions + timestamp**, edges encode **"assumes / depends-on"**, and the system **actively fires an alert** the instant a new decision falsifies the premise an earlier one relied on. *No reviewed competitor ships this combination.*

---

## 4. The framing line (and the honesty guardrail)

**Use:** *"Clash detection answers: do two objects occupy the same space right now? — geometric, single point in time, intent-blind. Keystone answers: does this new decision contradict the assumptions a prior decision relied on? — semantic, across time, rationale-aware. We're the temporal/semantic analogue of clash detection."*

**Guardrail (say this on stage to stay credible):** generic contradiction detection already exists (Alhena/Fini), and ADRs already have manual "superseded." The novelty is **NOT** "detecting conflicts" in the abstract — it is the **AEC decision-dependency graph + automatic premise-invalidation + rationale capture + golden-thread-native record**, which no reviewed competitor ships together.

---

## 5. Defensibility (for the judge / for a future business)

1. **Decision-dependency graph** as the core data model — a *reasoning* graph of decisions, not a flat log or an issue tracker.
2. **Active invalidation vs passive retrieval** — every incumbent is pull-based search; we *push* the alert the moment a premise is falsified. **The single sharpest differentiator.**
3. **Rationale + assumptions captured at the point of decision** — the "why" AEC tools systematically drop.
4. **AEC domain semantics** (disciplines, systems, phases) — the edge over horizontal memory.
5. **Compounding data moat** — the graph grows per project/firm; more decisions captured → more invalidations catchable. Frame defensibility *here*, not on the AI technique.

---

*Open competitive questions (worth a 30-min check before the demo) are in [06-open-questions.md](06-open-questions.md). Raw competitor research: [.research/research-competitors.md](../.research/research-competitors.md).*
