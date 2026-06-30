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
| "efficient memory storage and retrieval" | Bi-temporal **decision graph** — decisions as first-class nodes with rationale + assumptions; hybrid retrieval |
| "timely forgetting of outdated information" | **Active premise-invalidation** *(the differentiator — the one thing no competitor ships)* — supersede (not delete) a decision the moment a new one contradicts its premise |
| "recalling critical memories within limited context windows" | **Retrieve-to-budget** recall of only the currently-valid critical constraints, with correct abstention |

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
| — | [demo/demo-script.md](demo/demo-script.md) | The 3-scene "Maple Wharf" demo storyline + on-screen beats |
| — | [demo/transcripts/](demo/transcripts/) | The fictional meeting transcripts the agent ingests in the demo |
| — | [.research/](.research/) | Raw deep-research appendix (6 dimensions + adversarial verification + synthesis) |

---

## Status & provenance

- **2026-06-27** — Project initialized. Deep research completed (6 parallel research agents + adversarial fact-check + strategic synthesis). All docs below are written from that research.
- **2026-06-28** — Added the Singapore localization research (doc 07). Named the product **Trace**. Pushed to GitHub (private). Set the team's internal submission target to **7 July** (buffer before the 9 Jul hard deadline).
- **Confidence convention** used throughout: claims are tagged `[verified]` (primary source read), `[web search]` (relayed, not independently confirmed), or `[inference]`. The hackathon's official Devpost rules page renders empty to automated fetch, so a few logistics facts (exact demo-video length; whether Alibaba-Cloud *deployment* is mandatory) are flagged **unverified — confirm on the live page before the deadline.** See [docs/06-open-questions.md](docs/06-open-questions.md).
