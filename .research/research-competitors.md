## SUMMARY
The AEC tooling landscape is crowded with products that track design issues, clashes, RFIs, documents, and decisions-as-records — but my research found no product that does the specific four-part job you are targeting: capture a design decision WITH its rationale and timestamp AND a model of what downstream decisions depend on it AND actively flag when a later decision invalidates an earlier one. The incumbents split cleanly into two camps, neither of which closes the loop. (1) AEC coordination/issue tools (Revizto, Newforma Konekt/BIM Track, BIMcollab, Autodesk Construction Cloud/BIM 360) are excellent at geometric clash detection, spatially-anchored issues, and audit trails, but they track WHAT is wrong in the model, not WHY a choice was made or whether a past choice still holds. (2) Document-control/CDE platforms (Aconex, Asite, Procore) give you versioned correspondence and approval audit trails — a record of what happened, not a reasoning graph. AI startups (Helonic/ex-Articulate, Drawer AI, Bynaus, Togal, AutoRFP.ai) automate drawing review, issue/RFI generation, takeoff, and field docs — all forward-looking error detection, none tracking decision rationale or invalidation over time. AEC knowledge-management AI (Knowledge Architecture's Synthesis, Workorb) does retrieval/search over firm content, not decision dependency.

The closest conceptual analog is not in AEC at all: software Architecture Decision Records (ADRs), which capture decision + rationale + a superseded-by link. But ADRs are manual, software-only, and superseded is a human status flip — there is no automatic detection that a new decision has invalidated an old one, and no AEC/model awareness. On the horizontal side, AI second brain / memory products (Supermemory, Second Brain/MemoryOS, NotebookLM, Mem) increasingly ship typed decisions memory and even handle knowledge updates and contradictions, and a sub-genre of AI-knowledge-base tools (Alhena, Fini) does generic contradiction detection. None of these target AEC, understand disciplines/systems/model elements, or model design-decision dependencies. So detecting contradictions as an abstract capability is NOT novel — the defensible wedge is the combination: an AEC-domain decision-dependency graph that performs active premise-invalidation of downstream decisions.

The gap is real: decision + timestamp + rationale + active-invalidation-of-downstream is not served well by anyone. AEC tools have timestamp + audit but no rationale and no decision-dependency model; ADRs have rationale + manual supersede but no automation and no AEC; horizontal memory has typed decisions + contradiction handling but no AEC domain model and no dependency graph; decision logs (monday.com, Loqbooq, Jira) capture who/when/why but are static manual tables with no invalidation engine.

Your clash detection finds geometric conflicts; we find DECISION conflicts framing is valid and a strong hook — but sharpen it: clash detection answers do two objects occupy the same space right now? (geometry, single point in time, no intent). You answer does this new decision contradict the assumptions a past decision relied on? (semantics + time + rationale). It is the temporal/semantic analog of clash detection, not a like-for-like.

## KEY FINDINGS
- **[high]** AEC issue/coordination tools (Revizto, Newforma Konekt/BIM Track, BIMcollab, ACC/BIM 360) track issues, clashes and RFIs with spatial anchoring and audit trails, but capture issue STATUS, not the rationale behind a design choice or whether a past decision is still valid.
  - evidence: Revizto markets clash detection, automated grouping, automated issue creation, and issue tracking with a full audit trail captured until resolution; ACC lets teams convert clashes directly into trackable issues with assignees and due dates and link Issues to RFIs — all about defect/issue lifecycle, none describing decision rationale or invalidation.
  - source: https://revizto.com/product/integrated-issue-management ; https://www.autodesk.com/blogs/construction/bim-360-issues-to-rfis/
- **[high]** Clash detection is purely geometric/spatial and point-in-time — it has no concept of design intent or decision premises, validating (with refinement) the 'we find DECISION conflicts' framing.
  - evidence: Industry definitions describe clash detection as identifying physical/spatial conflicts between model elements (e.g., MEP vs structure) and converting those into issues; no source attributes intent- or rationale-awareness to clash engines.
  - source: https://revizto.com/resources/blog/clash-detection-in-bim ; https://strand-co.com/blogs/bim-clash-detection-process/
- **[high]** Document-control/CDE platforms (Aconex, Asite, Procore) provide versioned documents and full audit trails of correspondence/approvals — a record of WHAT happened, not a structured decision-rationale graph with dependency invalidation.
  - evidence: Aconex is described as a common data environment with full audit trails and structured Mail for RFIs/submittals captures metadata and keeps a full audit trail; framing is document/communication control, with no mention of decision-dependency or invalidation.
  - source: https://www.ingenious.build/blog-posts/top-aconex-alternatives-for-construction-teams ; https://www.capterra.com/compare/56250-220249/Procore-vs-Oracle-Aconex
- **[high]** AEC AI startups (Helonic/ex-Articulate, Drawer AI, Bynaus, Togal, AutoRFP.ai) focus on forward-looking error/issue detection and document automation, not longitudinal decision-rationale tracking or invalidation.
  - evidence: Helonic analyzes 2D PDF drawing sets for coordination conflicts, code compliance, missing information, and constructability issues across 10 categories and pushes issues as RFIs; Drawer AI does drawing package change analysis and error/advice/value-engineering reports; Bynaus auto-generates reports, tasks, RFIs, timecards, safety logs. None describe capturing decision rationale or detecting invalidated prior decisions.
  - source: https://helonic.com/ ; https://slashdot.org/software/comparison/Drawer-AI-vs-Togal.AI/ ; https://builtworlds.com/news/40-ai-driven-aec-solutions-to-know-in-2026/
- **[high]** AEC-specific knowledge management AI (Knowledge Architecture Synthesis, Workorb) does intranet/LMS/RAG search over firm content and past proposals — retrieval of existing knowledge, not a decision-dependency engine.
  - evidence: Synthesis is the leading intranet, LMS, and AI-powered search solution purpose-built for the AEC industry, with AI Search that summarizes the most relevant content; Workorb turns past proposals into a living knowledge graph. Both are retrieval/reuse, not active invalidation of design decisions.
  - source: https://www.knowledge-architecture.com/synthesis-ai-search ; https://www.workorb.com/blog/workorb-knowledge-management-aec-proposals
- **[high]** The closest conceptual analog is software Architecture Decision Records (ADRs): they capture decision + rationale + a superseded-by link — but supersession is a MANUAL human status change, with no automatic invalidation detection and no AEC/model awareness.
  - evidence: ADR status flows proposed to accepted to superseded with a link to the superseding ADR; tooling like adr-tools updates the old ADR status when you run a manual command. The act of marking something superseded is human-initiated, not detected.
  - source: https://adr.github.io/ ; https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
- **[medium]** Horizontal AI second brain/memory products increasingly ship typed decisions memory and even claim to handle contradictions — but none target AEC or model design-decision dependencies.
  - evidence: Second Brain ships with typed memory surfaces (decisions, facts, open loops, product state); Supermemory handles knowledge updates and contradictions, forgetting expired information. Search found no AEC-vertical features in these products — only community-built Claude Code skills using them as generic infrastructure.
  - source: https://www.iwoszapar.com/p/best-ai-second-brain-solutions ; https://github.com/supermemoryai/supermemory
- **[medium]** Generic contradiction detection already exists in AI knowledge bases, so detecting conflicts in the abstract is NOT novel — the defensible wedge is AEC-domain decision-dependency modeling + active downstream invalidation, not contradiction detection per se.
  - evidence: Tools like Alhena FAQ Conflict Detection and Fini find contradictions automatically; Gartner estimates ~70% of enterprise knowledge bases contain at least one pair of directly contradictory articles. But these operate on FAQ/document text, not on a graph of design decisions and their assumptions.
  - source: https://alhena.ai/blog/faq-conflict-detection-ai-knowledge-base/ ; https://www.usefini.com/guides/ai-knowledge-base-conflicting-answers
- **[high]** Decision logs are a recognized PM artifact (capturing what/who/when/why) with noted construction usage — but available tools are static manual tables with no automatic invalidation engine and no AEC model awareness.
  - evidence: A decision log captures what was decided, who made the decision, when it was made, and the reasoning behind it; tools cited are Jira/Trello/monday.com and Loqbooq (logs decisions in Slack). All manual entry; none described as detecting when a logged decision is invalidated by a later one.
  - source: https://monday.com/blog/project-management/decision-log/ ; https://loqbooq.app/
- **[medium]** The downstream-invalidation problem AEC firms feel is real and expensive, supporting demand: changes silently invalidate downstream decisions and drive rework.
  - evidence: Without traceability links, a change to a single requirement can silently invalidate downstream design decisions, test cases, and risk assessments; in AEC a minor adjustment in a dimension, a detail, or a system layout can trigger ripple effects across multiple disciplines; ~42% of institutional knowledge is unique to the individual who holds it: never written down.
  - source: https://www.jamasoftware.com/blog/change-impact-analysis-2/ ; https://dancumberlandlabs.com/blog/knowledge-management-engineering-firms/

## STRUCTURED
# Competitive Landscape: AEC Design-Decision Memory Agent

All "does NOT" entries are my inference from product positioning and the absence of any contrary claim in the sources (confidence: medium-high). No vendor I reviewed advertises rationale capture + automatic downstream-decision invalidation.

## Competitor Table

| Tool | Category | What it DOES | What it does NOT do |
|---|---|---|---|
| **Revizto** | A — BIM coordination / clash + issue tracking | Cloud real-time clash detection, automated clash grouping, auto issue creation from clashes, spatially-anchored 2D/3D issues, full audit trail to resolution, CDE connectors (ACC, Procore) | No capture of *why* a design choice was made; no decision-rationale model; no detection that a new decision invalidates an earlier one (tracks geometric/issue conflicts, not decision conflicts) |
| **Newforma Konekt (formerly BIM Track)** | A — BIM coordination / issue tracking + PM | Issue tracking in Revit/Navisworks 2D/3D, contextual issue reporting from clash results, real-time collaboration, "golden thread" project info mgmt | No rationale/assumptions capture per decision; no dependency graph of decisions; no active invalidation alerts |
| **BIMcollab (Zoom/Nexus)** | A — OpenBIM issue mgmt (BCF) | BCF-standard issue management, rule-based model checking, clash detection, IFC viewing, issue tracking across Revit/ARCHICAD/Tekla/Navisworks | BCF stores comments + screenshots on model elements, not decision rationale; no temporal invalidation of prior decisions |
| **Autodesk Construction Cloud / BIM 360 (Build/Forma)** | A — CDE + issues/RFIs/submittals | Clash to issue conversion, bi-directional Issue-RFI linking, RFIs/submittals/issues in one CDE with models, traceability issue to RFI to response to cost | Traces issue/RFI *workflow status*, not the reasoning behind design decisions; no engine to detect a superseded/invalidated design decision |
| **Oracle Aconex** | A — Document control / CDE | Versioned documents/specs, structured Mail for RFIs/submittals with metadata, full audit trails, multi-stakeholder workflows | Record of *correspondence and approvals*, not a structured decision-rationale graph; no downstream-decision invalidation |
| **Asite** | A — Document control / CDE | Cloud CDE, document control, workflow automation, supply-chain collaboration, lifecycle/asset information mgmt | Information/document lifecycle, not design-decision reasoning; no invalidation detection |
| **Procore** | A — Construction PM platform | Centralized docs, version control, submittals, RFIs, drawing mgmt, mobile field access | RFI/submittal workflow + docs; no rationale capture; no decision-dependency or invalidation engine |
| **Helonic (formerly Articulate, YC)** | A — AI drawing review / RFI gen | AI reviews 2D PDF sets for coordination conflicts, code compliance (NFPA 101, Title 24, ASHRAE 90.1), missing info, constructability across 10 categories; one-click push of issues as RFIs to Procore/ACC | Forward error-finding on a drawing set at a point in time; does NOT track decisions over time, their rationale, or detect that a later decision invalidates an earlier one |
| **Drawer AI** | A — AI drawing analysis | Drawing-package change analysis, error/advice/value-engineering reports, element classification, measurement extraction to avoid change orders | Analyzes drawings for errors/changes; no decision-rationale memory; no semantic decision-conflict detection |
| **Bynaus** | A — AI field documentation | Converts voice/photos/field activity into structured records; auto-generates reports, tasks, RFIs, timecards, safety/compliance docs | Field documentation automation; no design-decision rationale or invalidation tracking |
| **Togal.AI** | A — AI preconstruction takeoff | Auto detect/measure/label/compare spaces in drawings; drawing-set comparison; Togal.CHAT query of plans | Quantity takeoff/estimating; not a decision-memory or invalidation tool |
| **AutoRFP.ai** | A — AI RFI/RFP response | Generates RFI responses from approved content library + past responses; reuse/continuous improvement | Sales/response automation; no design-decision dependency or invalidation |
| **Knowledge Architecture — Synthesis** | A — AEC knowledge mgmt (intranet/LMS/AI search) | Purpose-built AEC intranet + LMS + AI Search (RAG) over firm content; integrates Deltek/Unanet/Newforma/Revit; "Knowledge Agents" beta | Retrieval/search and learning over existing firm knowledge; does NOT model per-project design decisions, rationale, or invalidation |
| **Workorb** | A — AEC proposal knowledge | Turns past proposals into a "living knowledge graph"; reuse across bids | Proposal/BD knowledge reuse; not project design-decision tracking or invalidation |
| **ADRs (adr-tools, ADR GitHub org)** | A-adjacent — software design-decision records | Captures decision + context + rationale + consequences; status proposed/accepted/**superseded** with link to superseding ADR | **Manual** supersession (human flips status); software-only, no AEC/model awareness; NO automatic detection that a new decision invalidates an old one |
| **Decision logs (monday.com, Loqbooq, Jira/Trello)** | A-adjacent — generic PM decision log | Manual capture of what/who/when/why, options considered, outcome; single source of truth; some construction usage | Static manual tables; no dependency graph; no automatic invalidation; not AEC-model-aware |
| **Supermemory** | B — horizontal AI memory engine/API | Persistent memory graph, RAG, connectors (Drive/Notion/OneDrive), "handles knowledge updates and contradictions," forgetting expired info | Horizontal; no AEC domain semantics; no design-decision dependency model; contradiction handling is generic fact-level, not downstream design-decision invalidation |
| **Second Brain / MemoryOS** | B — AI second brain | Typed memory surfaces incl. **decisions**, facts, open loops, product state; AI recalls without taught conventions | Personal-productivity vertical; no AEC awareness; no decision-dependency invalidation |
| **NotebookLM / Mem / Taskade Genesis** | B — AI note/second-brain | Upload docs, chat/query, auto-tag/link/recall, summarize | General PKM; no design-decision rationale graph; no invalidation engine; not AEC |
| **Alhena / Fini (AI KB conflict detection)** | B — AI knowledge-base contradiction detection | Automatically flag contradictory articles/answers in support KBs; knowledge graphs scoring freshness/authority | Operates on FAQ/support text, not a graph of design decisions + assumptions; no AEC; no downstream-decision invalidation |

## The Gap (who captures decision + timestamp + rationale + active-invalidation?)

Hypothesis confirmed at high confidence within the sources reviewed: **no single product does all four well.** The capability is split:

- **AEC issue/CDE tools** have timestamp + audit trail, but track *issues/clashes/documents*, not the *rationale* of a design decision, and have no decision-dependency model to invalidate. (high)
- **ADRs** have decision + rationale + supersede-link — the strongest conceptual match — but supersession is *manual*, it is *software-only*, and there is *no automatic invalidation detection*. (high)
- **Horizontal AI memory** has typed "decisions" + generic contradiction/update handling, but *no AEC domain model* (disciplines, systems, model elements) and *no design-decision dependency graph*. (medium)
- **Decision logs** capture who/when/why but are *static manual tables* with *no invalidation engine*. (high)

The unoccupied square: an AEC-aware system where decisions are first-class nodes carrying rationale + assumptions + timestamp, edges encode "depends-on / assumes," and the system *actively* fires an alert when a new decision falsifies the premise an earlier decision relied on. I found nobody advertising this combination.

## Framing: "clash detection finds geometric conflicts; we find DECISION conflicts"

Validated, and recommend this refinement for sharpness:
- **Clash detection** = "Do two physical objects occupy the same space right now?" — geometric, single point in time, intent-blind. (high; consistent across all sources)
- **You** = "Does this new decision contradict the assumptions a prior decision relied on?" — semantic + temporal + rationale-aware.
- Position it as the **temporal/semantic analog** of clash detection, not a like-for-like substitute. A clean one-liner: *"Clash detection catches when two ducts hit a beam. We catch when switching the frame from steel to concrete quietly breaks the MEP routing decision someone made three weeks ago — before it becomes a clash, an RFI, or rework."*
- Caveat to keep you honest with a judge: generic "contradiction detection" already exists in AI KBs (Alhena/Fini) and ADRs already have manual "superseded." So the novelty is NOT "detecting conflicts" in the abstract — it is the *AEC decision-dependency graph + automatic premise-invalidation*.

## Differentiation & Defensibility (for a hackathon judge)

What to claim (and the honest basis for each):
1. **Decision-dependency graph as the core data model** — decisions as nodes, "assumes/depends-on" as edges. Incumbents store issues, documents, or flat decision logs; none store a *reasoning graph* of design decisions. (Strong; differentiates from all of Group A and B.)
2. **Active invalidation vs passive retrieval** — every incumbent (CDE, Synthesis, second-brain) is pull-based search/storage; you *push* an alert the moment a decision's premise is falsified. This is the single sharpest differentiator. (Strong.)
3. **Rationale + assumptions captured at the point of decision** — the "why" and the "this assumed X" that AEC tools systematically drop (~42% of institutional knowledge is never written down). (Strong demand signal; medium evidence.)
4. **AEC domain semantics** — disciplines, systems, model elements, phases — that horizontal memory tools (Supermemory, Second Brain, NotebookLM) lack. This is your edge over Group B. (Strong vs B.)
5. **Data/compounding moat** — the decision graph grows per project and per firm; the more decisions captured, the more invalidations it can catch (network/data-moat effect). Frame defensibility here, not on the AI technique itself.

What to NOT overclaim (so a sharp judge can't puncture you): contradiction detection exists generically; ADRs already do manual supersede; decision logs already capture who/when/why. Your defensible combination = **AEC-aware decision-dependency graph + automatic downstream invalidation + rationale capture**, none of which any reviewed competitor ships together.

## Confidence & verification notes
- All findings are **[web search — not verified]** from result snippets; I did not fetch/render primary vendor pages beyond search summaries (devpost and some JS-heavy vendor pages render empty via fetch). Treat specific stat claims (e.g., Helonic "$30M+ rework prevented," "~42% institutional knowledge," "Gartner ~70%") as vendor/secondary claims, not independently verified.
- "Does NOT do X" rows are **[inference]** from positioning + absence of any contrary claim, not from a vendor explicitly disclaiming the feature. To harden before a judge, I'd want a hands-on check of one AEC tool (e.g., Revizto/ACC) and one second-brain (Supermemory) to confirm no hidden decision-invalidation feature.

## OPEN QUESTIONS
- Does any AEC tool have a non-advertised decision-invalidation feature? The 'does NOT' claims are inference from positioning, not vendor disclaimers — a hands-on trial of Revizto/ACC and Supermemory would harden this.
- Vendor stat claims (Helonic $30M+ rework prevented, ~42% institutional knowledge tacit, Gartner ~70% contradictory KBs) are unverified secondary numbers — confirm before citing to a judge.
- Is there an AEC-specific startup in stealth or recently funded (2025-2026) explicitly building design-decision/rationale memory? BuiltWorlds' '40 AI-Driven AEC Solutions 2026' list was not exhaustively reviewed item-by-item.
- How do owners/GCs currently reconstruct decision rationale for change-order/claim disputes today — is the buyer the design firm (avoid rework) or the owner (defend claims)? This shapes positioning.
- Does buildingSMART BCF or IFC have any emerging schema for decision rationale/provenance that a competitor could ride on?

## SOURCES
- https://www.newforma.com/newforma-konekt/bim-coordination/
- https://revizto.com/product/integrated-issue-management
- https://revizto.com/resources/blog/clash-detection-in-bim
- https://architosh.com/2025/08/inside-revizto-global-dominance-with-open-bim-coordination/
- https://www.autodesk.com/blogs/construction/bim-360-issues-to-rfis/
- https://bmsi.ai/bim-360-acc-issue-tracking-rfis-and-field-coordination/
- https://www.bimcollab.com/en/openbim/about-bcf/
- https://datadrivenaec.com/tools/bimcollab
- https://www.ingenious.build/blog-posts/top-aconex-alternatives-for-construction-teams
- https://www.capterra.com/compare/56250-220249/Procore-vs-Oracle-Aconex
- https://helonic.com/
- https://helonic.com/blog/articulate-rebrand-helonic
- https://builtworlds.com/news/40-ai-driven-aec-solutions-to-know-in-2026/
- https://slashdot.org/software/comparison/Drawer-AI-vs-Togal.AI/
- https://www.varseno.com/ai-transforming-construction-rfi-and-submittals/
- https://autorfp.ai/blog/rfi-software
- https://www.knowledge-architecture.com/synthesis-ai-search
- https://www.knowledge-architecture.com/synthesis-intranet
- https://www.workorb.com/blog/workorb-knowledge-management-aec-proposals
- https://dancumberlandlabs.com/blog/knowledge-management-engineering-firms/
- https://adr.github.io/
- https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
- https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- https://monday.com/blog/project-management/decision-log/
- https://loqbooq.app/
- https://www.jamasoftware.com/blog/change-impact-analysis-2/
- https://www.iwoszapar.com/p/best-ai-second-brain-solutions
- https://github.com/supermemoryai/supermemory
- https://blog.supermemory.ai/second-brain-apps-teams-ai-memory-apis/
- https://alhena.ai/blog/faq-conflict-detection-ai-knowledge-base/
- https://www.usefini.com/guides/ai-knowledge-base-conflicting-answers
- https://strand-co.com/blogs/bim-clash-detection-process/