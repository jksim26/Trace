# Trace: the Design-Decision Memory Agent for AEC

> **Name:** *Trace.* A *trace* is the unbroken line from every design decision back to *why* it was made. Trace keeps that line intact, and reasons along it: the moment a new decision breaks the premise an older one stood on, it argues the case and records the verdict.

**Hackathon:** Global AI Hackathon Series with Qwen Cloud (Alibaba Cloud / Devpost). **Track 1: MemoryAgent.** Hard deadline **9 July 2026, 14:00 PDT.** Team target: **submit 7 July.**

---

## The one-paragraph pitch

In a construction project the design brief evolves across dozens of meetings, but the industry records *what* was decided, never *why*. The rationale lives in email threads and people's heads, so months later nobody can say what a decision assumed, whether it still holds, or when it quietly stopped being true. **Trace is automation, not a tool.** It is an *ambient* decision-memory agent that sits in the design conversation and does the job, rather than a search box someone has to remember to open. It captures every decision and the reasoning behind it as the work happens (meetings, RFIs, minutes — or a note dropped into its **second-brain vault**) as a structured record: **decision, author, timestamp, rationale, and the assumptions it rests on.** Where every other memory agent merely *stores and retrieves*, Trace **reasons about decisions over time.** It knows at any moment which decisions are in force, which were superseded, and which the court rejected; it can **rewind to any past date** to reconstruct what was decided, and known, back then; it recalls only the still-valid constraints that matter, within a tight context budget; and the instant a new decision undercuts the premise an earlier one relied on, it convenes a **decision court**, where three agents argue the change for and against and a judge decides — and the verdict is a **real state transition on the record**, not prose. Nothing is ever deleted: superseded and rejected decisions are invalidated, not erased. What remains is a never-delete, attributable, **tamper-evident** record of *why* — every write is SHA-256 hash-chained, so any alteration of the log is detectable. That record is the defence Singapore's building law already assumes exists: under **Building Control Act s.9** the named design QP carries **personal, criminal** liability for design decisions, yet the only record the law prescribes (reg 22(e)) is structural-only, deviation-only and paper-era. Trace is the attributable, timestamped decision memory that liability regime has been missing.

> *Every memory agent remembers what was said. Trace remembers* why. *And the moment a new decision quietly breaks the premise an old one stood on, it does not just flag it: it argues both sides, records the verdict, and can still show you, years later, exactly what you knew and when.*

**Headline use case: handover.** When a senior engineer leaves, decades of design rationale walk out the door, and the standard one-to-two-month handover cannot transfer it. Because Trace has been capturing every decision and its *why* as the work happened (consensual capture-as-you-go, **not** surveillance), handover becomes automatic: the institutional memory is already on the record. `[inference]`

---

## The three pillars (these ARE Track 1's stated focus)

| Track 1 official wording | Trace feature |
|---|---|
| "efficient memory storage and retrieval" | Bi-temporal **decision store**: decisions as first-class records carrying rationale and assumptions, with never-delete supersession, plus **time-travel recall** (`get_valid_asof` reconstructs what was valid *and known* as of any date). |
| "timely forgetting of outdated information" | **Active premise-invalidation**, the differentiator no competitor ships: supersede (never delete) the moment a new decision contradicts an earlier one's premise, then convene a **decision court** where three Qwen roles (Proposer, Guardian, Judge) argue it out and write a defensible verdict. |
| "recalling critical memories within limited context windows" | **Retrieve-to-budget** recall of only the currently-valid critical constraints, with honest abstention, plus **multi-strategy** ranking (relevance, recency, importance, composite). |

---

## What runs today

The end-to-end loop is built and tested on a real Qwen stack, TDD throughout, with **147 offline tests**. Everything lives in [`Trace/`](Trace/):

| Module | What it does |
|---|---|
| `store.py` | The **foundation spine**: a never-delete, bi-temporal SQLite decision store with a real status machine (`valid / proposed / rejected / superseded`). Supersession closes `valid_to` and links `superseded_by`; the court's transitions (`reject_decision`, `adopt_decision`) land on the row (never a `DELETE`). Ids are **project-coded** (`408213-D-001` — the six-digit prefix names the project, so cited ids can't collide across projects). Every write appends to a **SHA-256 hash-chained audit log** (`verify_audit_chain()` detects any alteration). Ships `get_valid_asof` for **time-travel**, with the current view defined as `get_valid_asof(now)` so the two can never disagree. |
| `capture.py` | **Capture.** Qwen (`qwen-plus`) function-calling reads a meeting transcript and extracts each decision with its rationale, assumptions, and author. |
| `rulepack.py`, `rules/` | Deterministic **Singapore rule-packs, pluggable per code authority**: `rules/fire.yaml` is the SCDF pack (Cl 3.5.1 height **and** boundary limbs, Cl 3.5.4 low-rise Class 0, Cl 3.15.13 ACP core) and `rules/sg-bca/` is the BCA **Periodic Façade Inspection** pack (>13 m, >20 years, every 7 years, by an appointed Competent Person) — same engine, different authority. The gate that keeps the invalidation alert reliable on camera. |
| `invalidate.py` | **Invalidation alert**, the centrepiece — premise-aware: it names the *specific stored assumption* the new decision breaks, checks against **each project's own building context** (never a hardcoded building), and when the rule-pack is silent, an **LLM premise check** reads each prior decision's assumptions as the general fallback. |
| `court.py` | The **decision court**: three Qwen roles (Proposer, Guardian, Judge) deliberate a conflict and the verdict is a **real state transition** — REJECT marks the proposal `rejected` on the record, ALLOW adopts it and supersedes the decision it displaces. A rule-pack violation gates the verdict deterministically (reliable on camera); on rule-silent premise breaks the Judge **genuinely decides** (strict-JSON ruling, conservative REJECT fallback). Every verdict is **persisted** to the court record, joined to the judged row. |
| `recall.py`, `strategies.py`, `embeddings.py` | **Hybrid recall-to-budget.** Blends lexical overlap with a **Qwen text-embedding** semantic signal — so a paraphrase with no shared words ("make the exterior envelope cheaper" → the facade decision) is still recalled — then packs only the valid critical decisions within a token budget, cites them, and abstains honestly. The semantic half is additive and degrades to the deterministic lexical path with no key. Multi-strategy ranking (relevance, recency, importance, composite, hybrid). |
| `mcp_tools.py` | The four functions exposed as **Qwen-Agent custom tools** (LLM-driven), so a Qwen Assistant calls them itself. |
| `mcp_server.py` | The **real MCP server** (official `mcp` SDK, stdio) — eight **deterministic, keyless** tools over the Model Context Protocol: the never-delete record (`list_projects` / `list_decisions` / `get_decision`), bi-temporal `decisions_asof` time-travel, the rule-pack gate `check_compliance` (selects the SCDF or BCA pack, returns the clause + official link), `get_code_provision`, `verify_audit_chain` (recomputes the tamper-evident chain), and the persisted `court_records`. Any MCP client — Claude Desktop, a Qwen agent, an IDE — can ground on Trace's *certain* half with no key and no network. |
| `cli.py` | The four-scene **"Tanglin Rise" demo** (capture, then alert plus court, then recall with abstention, then time-travel) plus the staged ambient card. |
| `scenarios.py`, `rules/sg-bca/` | **Three Singapore projects, three companies, three code stories** — Tanglin Rise `408213` (95 m residential; SCDF fire rule-pack gates invalidation), Kranji Hub `517294` (industrial MEP; the LLM premise check catches what no rule covers), Pearl Vista `629481` (a 1999 tower under the BCA Periodic Façade Inspection regime — a second authority's pluggable rule-pack). Each store carries valid decisions, court-rejected proposals (real `rejected` status), superseded chains, and court records — real memory to recall. |
| `kb.py`, `kb/`, `vault_watcher.py` | **The second brain**: `kb/` is a plain markdown vault (Obsidian-compatible — the graph view IS the decision graph — but dependent on nothing). Drop a meeting note into `kb/<project>/inbox/` and the **vault watcher** ingests it as an immutable, audit-chained **episode**, captures its decisions, runs invalidation, and convenes the court; `kb.py` regenerates every decision, verdict and episode as a frontmatter+wikilink note (MADR-style status lifecycle), each carrying a `record_sha256` so `verify_vault` detects edited projections. Sources in, projections out — the store stays the only record. |
| `ambient.py`, `watch_rules.yaml` | **The ambient trigger — one brain, two worlds.** An allowlist matcher maps window/document titles to project contexts. Called by BOTH trigger paths, so the browser demo and the real desktop watcher are provably the same logic. |
| `watcher.py` | **The Windows desktop watcher**: polls the foreground window title (title bar only — no screen capture) and, on an allowlist match, pushes the document-open event to the bubble — open the Level 1 fire plan in Acrobat or Revit and Trace nudges you, unprompted. |
| `workspace.html` | **The simulated workspace** (`/workspace` on the bubble server): openable demo drawings (real PDFs in `demo/drawings/`) over the same matcher and the same live store — so judges experience the ambient nudge from a browser, zero install. Labeled honestly: the drawings are demo files; everything Trace does is live. |
| `bubble.py`, `bubble.html` | The **ambient bubble**: a tiny web app (Python standard library only) wired live to the engine, with a **project switcher** across the three scenarios. Its chat is ONE agent with ONE memory: a Qwen assistant **grounded in every project's decision + court records at once** (the switcher just sets the default context — ask about any project from anywhere), carrying the conversation history across switches, tolerates typos and follow-ups, cites decision ids, and still abstains on unrecorded decisions. Degrades to deterministic abstention without a key. |

---

## Quickstart

```bash
cd Trace
pip install -r requirements.txt
# create Trace/.env with a single line:  DASHSCOPE_API_KEY=sk-...   (Qwen Cloud, Singapore region)

python -m pytest         # all tests pass offline, no API key needed (the live smoke test auto-skips)
python cli.py            # the four-scene "Tanglin Rise" demo (add --pause to step through it)
python cli.py --offline  # the same demo with canned Qwen responses — no key, no network, cannot fail
python bubble.py         # the ambient bubble, a local web app with chat wired live to the engine
python mcp_tools.py      # a Qwen-Agent Assistant autonomously calling the tools
python mcp_server.py     # the deterministic, keyless MCP server (stdio) — register with any MCP client
# then open http://127.0.0.1:8765/workspace — open a drawing, watch the ambient nudge fire
python watcher.py        # (Windows) the real desktop watcher — same matcher, real window titles
python kb.py             # regenerate the kb/ second-brain vault from the stores (keyless, offline)
python vault_watcher.py pearl-vista  # watch kb/pearl-vista/inbox/ — drop a note, watch the court convene
```

- **`cli.py`**: Scene 1 capture, then Scene 2 the red invalidation alert plus the **decision court**'s REJECT verdict (the rejected proposal is preserved, never deleted), then Scene 3 recall-to-budget with the token meter plus abstention, then Scene 4 **bi-temporal time-travel**, then the staged ambient card. Capture and the court make real Qwen calls; the alert and abstention are deterministic.
- **`bubble.py`**: serves the Trace bubble at `http://127.0.0.1:8765` and opens it in your browser. On Windows, double-click `run_bubble.bat` (or `run_demo.bat` for the CLI).
- **`mcp_tools.py`**: a Qwen-Agent Assistant calls `capture_decision` then `check_invalidation` and concludes the PE-core ACP swap invalidates D-001. (`test_connection.py` is a live-API smoke check; it skips itself automatically when no key is set.)
- **`mcp_server.py`**: the deterministic half over the Model Context Protocol — point any MCP client at `python mcp_server.py` and it can `verify_audit_chain`, `decisions_asof`, `check_compliance`, and read the record with **no API key**. The tool functions are plain and importable, so the logic is unit-tested without the SDK.
- Windows `CERTIFICATE_VERIFY_FAILED`? `pip-system-certs` (already in requirements) bridges the Windows cert store into Python.

The module-by-module build is in [docs/superpowers/plans/](docs/superpowers/plans/) and [docs/superpowers/specs/](docs/superpowers/specs/); the design is in [docs/02-architecture.md](docs/02-architecture.md).

---

## Document map

| # | Doc | What it is |
|---|---|---|
| 00 | [docs/00-brief.md](docs/00-brief.md) | **The project brief:** problem, solution, users, why-now, hackathon fit, success criteria. |
| 01 | [docs/01-aec-direction.md](docs/01-aec-direction.md) | **The AEC case (strengthened):** pain points with hard numbers, the QP-liability wedge, worked examples. |
| 02 | [docs/02-architecture.md](docs/02-architecture.md) | **Architecture and framework:** data model, components, retrieval, the Qwen stack, Qwen-Agent tools. |
| 03 | [docs/03-hackathon-strategy.md](docs/03-hackathon-strategy.md) | **Strategy to win:** rules, judging-criteria alignment, MVP vs stretch scope, risks, build plan (7 Jul target). |
| 04 | [docs/04-qwen-tech-reference.md](docs/04-qwen-tech-reference.md) | **Build reference:** Qwen model IDs, context windows, embeddings, rerank, endpoints, credits. |
| 05 | [docs/05-competitive-landscape.md](docs/05-competitive-landscape.md) | **Why we win the room:** the competitor table and the precise unoccupied gap. |
| 06 | [docs/06-open-questions.md](docs/06-open-questions.md) | **Assumptions and decisions for you:** what was decided on your behalf and what to verify. |
| 07 | [docs/07-singapore-angle.md](docs/07-singapore-angle.md) | **The Singapore angle:** no golden thread, but QP personal criminal liability is the home-market wedge, with recommended framing and a localized demo. |
| 08 | [docs/08-tech-implementation.md](docs/08-tech-implementation.md) | **Tech implementation:** the technologies needed to build each part of Trace, with multiple implementation options per module. |
| 09 | [docs/09-manual-requirements.md](docs/09-manual-requirements.md) | **Manual requirements:** the human-only tasks (Qwen Cloud account, coupon, API key, live Devpost checks, deliverables) the AI build cannot do. |
| 10 | [docs/10-pitch-kit.md](docs/10-pitch-kit.md) | **Pitch kit:** the demo-video shot-list (the court is the money shot), the six-slide deck outline, and the final Devpost write-up. |
| diagram | [docs/diagram/architecture.png](docs/diagram/architecture.png) | **The system architecture diagram** (required submission artifact) — drawn as an architect's sheet: memory lifecycle, rule-gate + court, Alibaba Cloud footprint. Source: [architecture.html](docs/diagram/architecture.html). |
| demo | [demo/demo-script.md](demo/demo-script.md) | The "Tanglin Rise" (Singapore) demo storyline and on-screen beats. |
| demo | [demo/transcripts/](demo/transcripts/) | The fictional meeting transcripts the agent ingests in the demo. |
| research | [.research/](.research/) | Raw deep-research appendix (six dimensions, adversarial verification, synthesis). |

---

## Status & provenance

- **2026-06-27:** Project initialized. Deep research completed (6 parallel research agents, adversarial fact-check, strategic synthesis). All docs below are written from that research.
- **2026-06-28:** Added the Singapore localization research (doc 07). Named the product **Trace**. Pushed to GitHub (private). Set the team's internal submission target to **7 July** (buffer before the 9 Jul hard deadline).
- **2026-06-30:** Reframed the docs to the ambient decision-memory direction and built the **foundation spine**, the never-delete bi-temporal decision store, with its implementation plan.
- **2026-07-01:** Built the end-to-end loop, TDD: capture (Qwen function-calling), then the SCDF **rule-pack** gate, then the **invalidation alert**, then the **decision court** (three Qwen roles), then **recall-to-budget** with abstention, then **bi-temporal time-travel** and **multi-strategy** recall. Exposed the four functions as **Qwen-Agent custom tools**, shipped the **ambient bubble** (a live local web app) and the four-scene demo CLI, migrated the storyline to Singapore's **"Tanglin Rise"**, and wrote the pitch kit (doc 10). **46 offline tests.**
- **2026-07-02:** Council review (docs/reviews/), day-by-day pre-submission plan (doc 11), fresh-clone install fix, and pitch truth pass. **Read the live Devpost rules** (verbatim capture: [docs/12-devpost-official-rules.md](docs/12-devpost-official-rules.md)): video **< 3 min** on YouTube/Vimeo/Youku, **Alibaba Cloud deployment is mandatory** (proof = repo code file using Alibaba Cloud services), architecture diagram required, license must be visible in the repo's About section.
- **2026-07-10:** The all-Singapore refinement. (1) **UK removed entirely** — the Maple Wharf project, `rules/uk/` pack and every golden-thread/BSA pitch anchor are gone; the story now stands on Singapore's QP regime (Building Control Act s.9) end to end. (2) New third project **Pearl Vista** under the **BCA Periodic Façade Inspection** pack (`rules/sg-bca/`) — rule-packs now demonstrably pluggable per code authority. (3) **Verdicts became real state transitions**: a `rejected` status exists, the court stores/rejects/adopts the judged proposal (and supersedes what an ALLOW displaces), the LLM premise check actually reaches the court, proposals can't be laundered into force, and each project's building context is its own. (4) **Project-coded ids** (`408213-D-001`) end cross-project id collisions and make the bubble's citation filter a real hallucination check. (5) The **kb/ second brain**: an Obsidian-compatible markdown vault — inbox notes ingest as audit-chained episodes through capture → invalidation → court; decisions/verdicts/episodes project back as wikilinked notes. **147 offline tests.**
- **Confidence convention** used throughout: claims are tagged `[verified]` (primary source read), `[web search]` (relayed, not independently confirmed), or `[inference]`. The former VERIFY-LIVE logistics items are now settled by the 2026-07-02 live rules read; see [docs/12-devpost-official-rules.md](docs/12-devpost-official-rules.md) and [docs/09-manual-requirements.md](docs/09-manual-requirements.md) §B.
