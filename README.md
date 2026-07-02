# Trace — the Design-Decision Memory Agent for AEC

> **Name:** *Trace*.
> A *trace* is the unbroken line from every design decision back to *why* it was made. This agent keeps that line intact — and shouts the moment a new decision quietly breaks an old one.

**Hackathon:** Global AI Hackathon Series with Qwen Cloud (Alibaba Cloud / Devpost) · **Track 1 — MemoryAgent** · hard deadline **9 July 2026, 14:00 PDT** · **team target: submit 7 July**.

---

## The one-paragraph pitch

In a construction project, the design brief evolves across dozens of meetings, but nobody records *which decision changed, when, and why*. By the time the drawings are issued, the design intent is blurred — and a budget decision made in March silently contradicts a fire-safety decision made in January. **Trace is automation, not a tool** — an *ambient* decision-memory agent that sits in the room and does the job rather than a search box someone must remember to open. It captures every design decision and its rationale as it is made (meetings, RFIs, minutes-of-meeting) and stores each as a structured record (**decision + timestamp + author + rationale + the assumptions it rests on**); it always knows which decisions are currently valid versus superseded; and — the part nobody else does — it *actively pushes an alert the instant a new decision falsifies the premise an earlier decision relied on*. It surfaces the right critical constraints proactively and in-context under a tight budget, and it never deletes: superseded decisions are invalidated, not erased, producing exactly the immutable, attributable audit trail the UK Building Safety Act's "golden thread" now makes **legally mandatory** for higher-risk buildings.

> *"Clash detection catches two ducts hitting a beam. We catch the moment a cost decision quietly breaks a fire decision someone made seven weeks ago — before it becomes an RFI, a Gateway failure, or a tragedy."*

**Headline use case — handover.** When a senior engineer leaves, decades of design rationale walk out the door and the standard one-to-two-month handover can't transfer it. Because Trace has been capturing every decision and its *why* as the work happened — consensual capture-as-you-go, **not** surveillance — handover becomes automatic: the institutional memory is already on the record. `[inference]`

---

## The three pillars (these ARE Track 1's stated focus)

| Track 1 official wording | Trace feature |
|---|---|
| "efficient memory storage and retrieval" | Bi-temporal **decision store** — decisions as first-class records with rationale + assumptions; never-delete supersession, plus **time-travel recall** (`get_valid_asof` — reconstruct what was valid *and known* as of any date) |
| "timely forgetting of outdated information" | **Active premise-invalidation** *(the differentiator — the one thing no competitor ships)* — supersede (not delete) the moment a new decision contradicts an earlier one's premise, then convene a **decision court**: three Qwen roles (Proposer / Guardian / Judge) argue it out and write a defensible verdict |
| "recalling critical memories within limited context windows" | **Retrieve-to-budget** recall of only the currently-valid critical constraints, with honest abstention — and **multi-strategy** ranking (relevance / recency / importance / composite) |

---

## What runs today

The end-to-end loop is built and tested on a real Qwen stack — TDD throughout, **46 offline tests**. Everything lives in [`Trace/`](Trace/):

| Module | What it does |
|---|---|
| `store.py` | The **foundation spine** — a never-delete, bi-temporal SQLite decision store; supersession closes `valid_to` and links `superseded_by` (never a `DELETE`). Ships `get_valid_asof` for **time-travel**. |
| `capture.py` | **Capture** — Qwen (`qwen-plus`) function-calling reads a meeting transcript and extracts each decision + rationale + assumptions + author. |
| `rulepack.py` · `rules/fire.yaml` | The deterministic **SCDF rule-pack** — the gate that keeps the invalidation alert reliable on camera (it can't mis-fire). |
| `invalidate.py` | **Invalidation alert** — the centrepiece; fires the instant a new decision breaks a prior one's premise, with a plain-English blast radius. |
| `court.py` | The **decision court** — three Qwen roles (Proposer / Guardian / Judge) deliberate a rule-pack-gated conflict and write the verdict a personally-liable QP can stand behind. |
| `recall.py` · `strategies.py` | **Recall-to-budget** — packs only the valid critical decisions within a token budget, cites them, and abstains honestly; multi-strategy ranking (relevance / recency / importance / composite). |
| `mcp_tools.py` | The four functions exposed as **Qwen-Agent MCP tools**, so a Qwen Assistant calls them itself. |
| `cli.py` | The 4-scene **"Tanglin Rise" demo** (capture → alert + court → recall + abstention → time-travel) plus the staged ambient card. |
| `bubble.py` · `bubble.html` | The **ambient bubble** — a tiny local web app (Python stdlib only) wired live to the engine; its chat box is a real `recall_decisions` call. |

---

## Quickstart

```bash
cd Trace
pip install -r requirements.txt
# create Trace/.env with a single line:  DASHSCOPE_API_KEY=sk-...   (Qwen Cloud, Singapore region)

python -m pytest --ignore=test_connection.py   # 46 tests, no API key needed (the LLM is mocked)
python cli.py            # the 4-scene "Tanglin Rise" demo (add --pause to step through it)
python bubble.py         # the ambient bubble — a local web app, chat wired live to the engine
python mcp_tools.py      # a Qwen-Agent Assistant autonomously calling the tools
```

- **`cli.py`** — Scene 1 capture → Scene 2 the red invalidation alert + the **decision court**'s REJECT verdict (the rejected proposal is preserved, never deleted) → Scene 3 recall-to-budget with the token meter + abstention → Scene 4 **bi-temporal time-travel** → the staged ambient card. Capture and the court make real Qwen calls; the alert and abstention are deterministic.
- **`bubble.py`** — serves the Trace bubble at `http://127.0.0.1:8765` and opens it in your browser. Windows: double-click `run_bubble.bat` (or `run_demo.bat` for the CLI).
- **`mcp_tools.py`** — a Qwen-Agent Assistant calls `capture_decision` then `check_invalidation` and concludes the PE-core ACP swap invalidates D-001. (`test_connection.py` is a one-line live-API smoke check, so it's excluded above — it needs the key.)
- Windows `CERTIFICATE_VERIFY_FAILED`? `pip-system-certs` (already in requirements) bridges the Windows cert store into Python.

The module-by-module build is in [docs/superpowers/plans/](docs/superpowers/plans/) and [docs/superpowers/specs/](docs/superpowers/specs/); the design in [docs/02-architecture.md](docs/02-architecture.md).

---

## Document map

| # | Doc | What it is |
|---|---|---|
| 00 | [docs/00-brief.md](docs/00-brief.md) | **The project brief** — problem, solution, users, why-now, hackathon fit, success criteria |
| 01 | [docs/01-aec-direction.md](docs/01-aec-direction.md) | **The AEC case (strengthened)** — pain points with hard numbers, the golden-thread wedge, worked examples |
| 02 | [docs/02-architecture.md](docs/02-architecture.md) | **Architecture & framework** — data model, components, retrieval, the Qwen stack, MCP tools |
| 03 | [docs/03-hackathon-strategy.md](docs/03-hackathon-strategy.md) | **Strategy to win** — rules, judging-criteria alignment, MVP vs stretch scope, risks, build plan (7 Jul target) |
| 04 | [docs/04-qwen-tech-reference.md](docs/04-qwen-tech-reference.md) | **Build reference** — Qwen model IDs, context windows, embeddings, rerank, endpoints, credits |
| 05 | [docs/05-competitive-landscape.md](docs/05-competitive-landscape.md) | **Why we win the room** — competitor table and the precise unoccupied gap |
| 06 | [docs/06-open-questions.md](docs/06-open-questions.md) | **Assumptions & decisions for you** — what I decided on your behalf and what to verify |
| 07 | [docs/07-singapore-angle.md](docs/07-singapore-angle.md) | **The Singapore angle** — no golden thread, but QP personal criminal liability is the home-market wedge; recommended framing + localized demo |
| 08 | [docs/08-tech-implementation.md](docs/08-tech-implementation.md) | **Tech implementation** — What technologies are needed to build each part of Trace, with multiple implementation options per module |
| 09 | [docs/09-manual-requirements.md](docs/09-manual-requirements.md) | **Manual requirements** — the human-only tasks (Qwen Cloud account, coupon, API key, live Devpost checks, deliverables) the AI build can't do |
| 10 | [docs/10-pitch-kit.md](docs/10-pitch-kit.md) | **Pitch kit** — the ≤3-min demo-video shot-list (court = the money shot), the 6-slide deck outline, and the final Devpost write-up |
| — | [demo/demo-script.md](demo/demo-script.md) | The "Tanglin Rise" (Singapore) demo storyline + on-screen beats |
| — | [demo/transcripts/](demo/transcripts/) | The fictional meeting transcripts the agent ingests in the demo |
| — | [.research/](.research/) | Raw deep-research appendix (6 dimensions + adversarial verification + synthesis) |

---

## Status & provenance

- **2026-06-27** — Project initialized. Deep research completed (6 parallel research agents + adversarial fact-check + strategic synthesis). All docs below are written from that research.
- **2026-06-28** — Added the Singapore localization research (doc 07). Named the product **Trace**. Pushed to GitHub (private). Set the team's internal submission target to **7 July** (buffer before the 9 Jul hard deadline).
- **2026-06-30** — Reframed the docs to the ambient decision-memory direction and built the **foundation spine** — the never-delete, bi-temporal decision store — with its implementation plan.
- **2026-07-01** — Built the end-to-end loop, TDD: capture (Qwen function-calling) → SCDF **rule-pack** gate → **invalidation alert** → **decision court** (three Qwen roles) → **recall-to-budget** with abstention → **bi-temporal time-travel** + **multi-strategy** recall. Exposed the four functions as **Qwen-Agent MCP tools**, shipped the **ambient bubble** (a live local web app) and the 4-scene demo CLI, migrated the storyline to Singapore's **"Tanglin Rise"**, and wrote the pitch kit (doc 10). **46 offline tests**.
- **Confidence convention** used throughout: claims are tagged `[verified]` (primary source read), `[web search]` (relayed, not independently confirmed), or `[inference]`. The hackathon's official Devpost rules page renders empty to automated fetch, so a few logistics facts (exact demo-video length; whether Alibaba-Cloud *deployment* is mandatory) are flagged **unverified — confirm on the live page before the deadline.** See [docs/06-open-questions.md](docs/06-open-questions.md).
