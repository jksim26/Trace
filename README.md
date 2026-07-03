# Trace: the Design-Decision Memory Agent for AEC

> **Name:** *Trace.* A *trace* is the unbroken line from every design decision back to *why* it was made. Trace keeps that line intact, and reasons along it: the moment a new decision breaks the premise an older one stood on, it argues the case and records the verdict.

**Hackathon:** Global AI Hackathon Series with Qwen Cloud (Alibaba Cloud / Devpost). **Track 1: MemoryAgent.** Hard deadline **9 July 2026, 14:00 PDT.** Team target: **submit 7 July.**

---

## The one-paragraph pitch

In a construction project the design brief evolves across dozens of meetings, but the industry records *what* was decided, never *why*. The rationale lives in email threads and people's heads, so months later nobody can say what a decision assumed, whether it still holds, or when it quietly stopped being true. **Trace is automation, not a tool.** It is an *ambient* decision-memory agent that sits in the design conversation and does the job, rather than a search box someone has to remember to open. It captures every decision and the reasoning behind it as the work happens (meetings, RFIs, minutes) as a structured record: **decision, author, timestamp, rationale, and the assumptions it rests on.** Where every other memory agent merely *stores and retrieves*, Trace **reasons about decisions over time.** It knows at any moment which decisions are valid and which are superseded; it can **rewind to any past date** to reconstruct what was decided, and known, back then; it recalls only the still-valid constraints that matter, within a tight context budget; and the instant a new decision undercuts the premise an earlier one relied on, it convenes a **decision court**, where three agents argue the change for and against and a judge writes the verdict and its reasoning. Nothing is ever deleted: superseded decisions are invalidated, not erased. What remains is a never-delete, attributable, **tamper-evident** record of *why* — every write is SHA-256 hash-chained, so any alteration of the log is detectable, the "golden thread" the UK Building Safety Act now makes **legally mandatory**, and the defence a personally and criminally liable engineer has otherwise never had.

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

The end-to-end loop is built and tested on a real Qwen stack, TDD throughout, with **83 offline tests**. Everything lives in [`Trace/`](Trace/):

| Module | What it does |
|---|---|
| `store.py` | The **foundation spine**: a never-delete, bi-temporal SQLite decision store. Supersession closes `valid_to` and links `superseded_by` (never a `DELETE`). Every write appends to a **SHA-256 hash-chained audit log** (`verify_audit_chain()` detects any alteration). Ships `get_valid_asof` for **time-travel**. |
| `capture.py` | **Capture.** Qwen (`qwen-plus`) function-calling reads a meeting transcript and extracts each decision with its rationale, assumptions, and author. |
| `rulepack.py`, `rules/fire.yaml` | The deterministic **SCDF rule-pack** — four rules from the primary-source research (Cl 3.5.1 height **and** boundary limbs, Cl 3.5.4 low-rise Class 0, Cl 3.15.13 ACP core): the gate that keeps the invalidation alert reliable on camera. |
| `invalidate.py` | **Invalidation alert**, the centrepiece — premise-aware: it names the *specific stored assumption* the new decision breaks, and when the rule-pack is silent, an **LLM premise check** reads each prior decision's assumptions as the general fallback. |
| `court.py` | The **decision court**: three Qwen roles (Proposer, Guardian, Judge) deliberate a rule-pack-gated conflict, write the reasoning a personally-liable QP can stand behind, and **persist every verdict** to the court record. |
| `recall.py`, `strategies.py` | **Recall-to-budget.** Packs only the valid critical decisions within a token budget, cites them, and abstains honestly. Multi-strategy ranking (relevance, recency, importance, composite). |
| `mcp_tools.py` | The four functions exposed as **Qwen-Agent custom tools**, so a Qwen Assistant calls them itself (MCP-protocol exposure is roadmap). |
| `cli.py` | The four-scene **"Tanglin Rise" demo** (capture, then alert plus court, then recall with abstention, then time-travel) plus the staged ambient card. |
| `scenarios.py`, `rules/uk/` | **Three demo projects, three companies, three code regimes** — SG high-rise (SCDF rule-gated), SG industrial MEP (LLM-premise-check story), UK residential (a separate pluggable rule-pack: reg 7(2) combustible ban). Each store carries valid decisions, rejected proposals, superseded chains, and court records — real memory to recall. |
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
```

- **`cli.py`**: Scene 1 capture, then Scene 2 the red invalidation alert plus the **decision court**'s REJECT verdict (the rejected proposal is preserved, never deleted), then Scene 3 recall-to-budget with the token meter plus abstention, then Scene 4 **bi-temporal time-travel**, then the staged ambient card. Capture and the court make real Qwen calls; the alert and abstention are deterministic.
- **`bubble.py`**: serves the Trace bubble at `http://127.0.0.1:8765` and opens it in your browser. On Windows, double-click `run_bubble.bat` (or `run_demo.bat` for the CLI).
- **`mcp_tools.py`**: a Qwen-Agent Assistant calls `capture_decision` then `check_invalidation` and concludes the PE-core ACP swap invalidates D-001. (`test_connection.py` is a live-API smoke check; it skips itself automatically when no key is set.)
- Windows `CERTIFICATE_VERIFY_FAILED`? `pip-system-certs` (already in requirements) bridges the Windows cert store into Python.

The module-by-module build is in [docs/superpowers/plans/](docs/superpowers/plans/) and [docs/superpowers/specs/](docs/superpowers/specs/); the design is in [docs/02-architecture.md](docs/02-architecture.md).

---

## Document map

| # | Doc | What it is |
|---|---|---|
| 00 | [docs/00-brief.md](docs/00-brief.md) | **The project brief:** problem, solution, users, why-now, hackathon fit, success criteria. |
| 01 | [docs/01-aec-direction.md](docs/01-aec-direction.md) | **The AEC case (strengthened):** pain points with hard numbers, the golden-thread wedge, worked examples. |
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
- **Confidence convention** used throughout: claims are tagged `[verified]` (primary source read), `[web search]` (relayed, not independently confirmed), or `[inference]`. The former VERIFY-LIVE logistics items are now settled by the 2026-07-02 live rules read; see [docs/12-devpost-official-rules.md](docs/12-devpost-official-rules.md) and [docs/09-manual-requirements.md](docs/09-manual-requirements.md) §B.
