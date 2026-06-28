# Keystone — the Design-Decision Memory Agent for AEC

> **Working name:** *Keystone* (provisional — see [docs/06-open-questions.md](docs/06-open-questions.md) for alternatives).
> A keystone is the one stone an arch depends on. This agent remembers the design decisions a project depends on — and shouts the moment a new decision quietly breaks an old one.

**Hackathon:** Global AI Hackathon Series with Qwen Cloud (Alibaba Cloud / Devpost) · **Track 1 — MemoryAgent** · submission deadline **9 July 2026, 14:00 PDT**.

---

## The one-paragraph pitch

In a construction project, the design brief evolves across dozens of meetings, but nobody records *which decision changed, when, and why*. By the time the drawings are issued, the design intent is blurred — and a budget decision made in March silently contradicts a fire-safety decision made in January. **Keystone** is a memory agent that ingests design-meeting conversations, stores every decision as a structured record (**decision + timestamp + author + rationale + the assumptions it rests on**), and — the part nobody else does — *actively fires an alert the instant a new decision falsifies the premise an earlier decision relied on*. It recalls the right critical constraints under a tight context budget, and it never deletes: superseded decisions are invalidated, not erased, producing exactly the immutable, attributable audit trail the UK Building Safety Act's "golden thread" now makes **legally mandatory** for higher-risk buildings.

> *"Clash detection catches two ducts hitting a beam. We catch the moment a cost decision quietly breaks a fire decision someone made seven weeks ago — before it becomes an RFI, a Gateway failure, or a tragedy."*

---

## The three pillars (these ARE Track 1's stated focus)

| Track 1 official wording | Keystone feature |
|---|---|
| "efficient memory storage and retrieval" | Bi-temporal **decision graph** — decisions as first-class nodes with rationale + assumptions; hybrid retrieval |
| "timely forgetting of outdated information" | **Active premise-invalidation** — supersede (not delete) a decision the moment a new one contradicts its premise |
| "recalling critical memories within limited context windows" | **Retrieve-to-budget** recall of only the currently-valid critical constraints, with correct abstention |

---

## Document map

| # | Doc | What it is |
|---|---|---|
| 00 | [docs/00-brief.md](docs/00-brief.md) | **The project brief** — problem, solution, users, why-now, hackathon fit, success criteria |
| 01 | [docs/01-aec-direction.md](docs/01-aec-direction.md) | **The AEC case (strengthened)** — pain points with hard numbers, the golden-thread wedge, worked examples |
| 02 | [docs/02-architecture.md](docs/02-architecture.md) | **Architecture & framework** — data model, components, retrieval, the Qwen stack, MCP tools |
| 03 | [docs/03-hackathon-strategy.md](docs/03-hackathon-strategy.md) | **Strategy to win** — rules, judging-criteria alignment, MVP vs stretch scope, risks, 12-day plan |
| 04 | [docs/04-qwen-tech-reference.md](docs/04-qwen-tech-reference.md) | **Build reference** — Qwen model IDs, context windows, embeddings, rerank, endpoints, credits |
| 05 | [docs/05-competitive-landscape.md](docs/05-competitive-landscape.md) | **Why we win the room** — competitor table and the precise unoccupied gap |
| 06 | [docs/06-open-questions.md](docs/06-open-questions.md) | **Assumptions & decisions for you** — what I decided on your behalf and what to verify |
| 07 | [docs/07-singapore-angle.md](docs/07-singapore-angle.md) | **The Singapore angle** — no golden thread, but QP personal criminal liability is the home-market wedge; recommended framing + localized demo |
| — | [demo/demo-script.md](demo/demo-script.md) | The 3-scene "Maple Wharf" demo storyline + on-screen beats |
| — | [demo/transcripts/](demo/transcripts/) | The fictional meeting transcripts the agent ingests in the demo |
| — | [.research/](.research/) | Raw deep-research appendix (6 dimensions + adversarial verification + synthesis) |

---

## Status & provenance

- **2026-06-27** — Project initialized. Deep research completed (6 parallel research agents + adversarial fact-check + strategic synthesis). All docs below are written from that research.
- **Confidence convention** used throughout: claims are tagged `[verified]` (primary source read), `[web search]` (relayed, not independently confirmed), or `[inference]`. The hackathon's official Devpost rules page renders empty to automated fetch, so a few logistics facts (exact demo-video length; whether Alibaba-Cloud *deployment* is mandatory) are flagged **unverified — confirm on the live page before the deadline.** See [docs/06-open-questions.md](docs/06-open-questions.md).
