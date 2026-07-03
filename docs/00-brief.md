# 00 · Project Brief — Trace

*Design-Decision Memory Agent for AEC · Qwen Cloud Hackathon, Track 1 (MemoryAgent)*
*Written 2026-06-27. Confidence tags: `[verified]` / `[web search]` / `[inference]`.*

---

## 1. The problem in one breath

On a building project, the **design brief is a living thing** — it changes across dozens of meetings as the client, architect, and consultants make decisions. But the industry records *what* was decided, not *why*. Rationale and assumptions live in email threads, half-attended meeting minutes, and people's heads — and "it's quite likely that nobody who is there at the very beginning of a project is involved at the end." `[web search — Levitt Bernstein architect, AJ roundtable]`

So three failures happen on every project:

1. **The brief silently goes stale.** A decision made in January assumes the building stays a certain way. In March, a value-engineering decision quietly contradicts that assumption — and nobody connects the two until it surfaces months later as an RFI, a clash, a change order, or a failed regulatory gateway.
2. **The "why" evaporates.** Six months later someone asks *"why did we choose terracotta?"* and the answer — *"because it's a higher-risk building and combustible cladding is illegal over 18 m"* — is gone. The team re-litigates a settled decision, or worse, reverses it without knowing what it was protecting.
3. **There is no defensible record.** When a dispute or a safety review comes, there is no immutable, attributable trail of who decided what, when, and why.

These compound at **handover.** When a senior leaves, the rationale walks out the door with them — a clean one-to-two-month handover is rarely possible, and the incoming lead inherits live decisions with no idea what they were protecting. Because Trace captures decisions *as they are made* — consensual capture-as-you-go, never surveillance — the handover record builds itself continuously instead of being reconstructed under pressure at the end. `[inference]`

This is not a niche annoyance. It is the **information-management failure that every architecture and engineering firm actually faces**, and — uniquely for our wedge — the UK government has already **legislated** that it must be fixed (see §4).

## 2. What Trace is

**Automation, not a tool.** You don't *pick Trace up and query it* — it runs ambiently alongside the design conversation, capturing and reconciling decisions as they are made, and it **pushes** the relevant knowledge to you in context instead of waiting to be asked. Active push, not passive pull, is *the single sharpest differentiator* (see [05-competitive-landscape.md](05-competitive-landscape.md)).

A **memory agent that sits alongside the design conversation** and does four things no existing tool does together:

1. **Captures** each design decision as a structured record: `decision · timestamp · author · discipline · rationale · the assumptions it rests on · the brief item it changes`.
2. **Detects** — actively, unprompted — when a *new* decision falsifies the **premise** an *earlier* decision relied on, and fires a conflict alert *in the meeting*, before the contradiction propagates into rework.
3. **Recalls** the right currently-valid critical constraints on demand, fitting them into a tight context budget, and correctly **abstains** ("no decision on record") instead of inventing answers.
4. **Preserves** history immutably: a superseded decision is invalidated, not deleted, leaving a queryable "changed by whom, when, why" chain.

Under the hood that is a **five-part memory architecture** — a short-term conversation buffer, a long-term decision graph + vector index, write logic, retrieval-to-budget, and a *two-tier* forgetting logic whose active **premise-invalidation** tier (item 2 above) is the box almost every memory system leaves empty (full treatment in [02-architecture.md](02-architecture.md)). `[inference]`

**The sharpest way to say it:** *Clash detection finds geometric conflicts — two objects in the same space, right now. Trace finds **decision conflicts** — a new choice that breaks the assumptions of an old one, across time. It is the temporal/semantic analogue of clash detection.* `[inference, validated against competitor research]`

## 3. Who it's for

- **Primary user (build & demo for this one):** the **design team** — architect / lead designer, project architect, and the discipline consultants (structural, MEP, fire, facade) — plus the project's **Information Manager / BIM manager** who owns the record. They feel the rework pain and carry the professional-liability risk.
- **Secondary buyers:** the **principal designer / principal contractor** (statutory dutyholders under UK CDM/BSA), and the **client/owner** who needs a defensible decision trail for disputes and claims.

## 4. Why now — the wedge that makes this mandatory, not optional

> **🇸🇬 Singapore note (added 2026-06-28):** You're a Singapore team facing APAC judges. Singapore has **no** golden thread — but its **Qualified Person regime makes a named architect/engineer personally and criminally liable** for design decisions while giving them only fragmented structural paper to defend themselves. That's a *home-market* wedge, arguably sharper than the UK frame. **Recommended lead = Singapore (QP liability) + China (lifelong quality responsibility) + UK golden thread as a one-line precedent.** Full analysis and the exact rewrite list: **[07-singapore-angle.md](07-singapore-angle.md)**. Don't rewrite this section until you've locked the framing (decision #2 in [06](06-open-questions.md)).

After the Grenfell Tower fire (2017, 72 deaths), Dame Judith Hackitt's review *Building a Safer Future* (2018) named our exact problem in its own words:

> *"Why design and construction decisions were made, and by whom, may not be recorded, and the final records of the design may not reflect what has actually been built."* `[web search — gov.uk Hackitt report]`

That finding became law. The **Building Safety Act 2022** mandates a **"golden thread of information"** for **higher-risk buildings** (≥ 18 m or ≥ 7 storeys with ≥ 2 dwellings). The golden thread must show **who did what, when, and why**, and every entry must be **attributable to a named user, timestamped, and immutable** (historical states preserved, not overwritten). `[web search — ICE, Construction Leadership Council guidance]`

**Read that data model again — *named user, timestamped, immutable, with the why* — it is Trace's schema, line for line.** This is what turns the project from "a cool memory demo" into infrastructure a whole class of buildings is now *legally required* to maintain, and it generalises beyond the UK as a professional-liability defence everywhere. This is the highest-confidence, highest-impact claim we have, and it should lead every judge-facing surface.

## 5. Why this is the *right* Track-1 entry (not a stretch)

The Track 1 brief asks for an agent with "persistent memory… efficient memory storage and retrieval, timely forgetting of outdated information, and recalling critical memories within limited context windows." `[verified — qwencloud.com challenge page]` Trace's three pillars are a **one-to-one map** onto that wording (see README table). Most Track-1 entrants will build a generic personal-assistant memory ("remembers your coffee order"). Trace takes the same core mechanics — store, forget-the-obsolete, recall-under-budget — and points them at a **real, expensive, legally-backed industry problem**. That is precisely how you win the 25% "Problem Value & Impact" criterion that generic entries leave on the table. `[inference]`

## 6. Feasibility — why this is buildable in the time we have

The technical spine has **no unsolved research problem in it** — it is `memory store + decay/invalidation mechanism + retrieval ranking`, all of which have 2024–2026 reference implementations (Graphiti's bi-temporal graph for invalidation, Generative-Agents/Mem0 composite scoring for retrieval, MemGPT/Letta for context budgeting — see [docs/02-architecture.md](02-architecture.md)). The demo runs on **fictional design-meeting transcripts** we author, so we control the storyline and can make the centrepiece alert deterministic. The whole thing fits on the Qwen stack we're required to use anyway (qwen3.7-max for reasoning, text-embedding-v4 + qwen3-rerank for retrieval, Qwen-Agent for MCP tools — see [docs/04-qwen-tech-reference.md](04-qwen-tech-reference.md)).

## 7. Success criteria (definition of done)

The submission is "done" when the demo can show, end-to-end, on the authored transcripts:

- **C1 — Capture:** ingest a meeting transcript → produce a correct structured decision record with rationale + assumptions + author + timestamp. *Verify: the record reads back accurately.*
- **C2 — Invalidate:** when a later transcript contains a contradicting decision, the agent **fires a conflict alert unprompted**, names the prior decision it breaks, and explains why. *Verify: the alert fires reliably on the demo storyline.*
- **C3 — Recall under budget:** answer "why X, and can we still change it?" by pulling only the relevant currently-valid decisions into a visible token budget, **and abstain** when no decision exists. *Verify: the context-budget meter and the abstention case both work on camera.*
- **C4 — Immutable trail:** show that the superseded decision is preserved with a `superseded_by` link, not erased. *Verify: the audit/history view walks the chain.*
- **C5 — Qwen-native + agent-callable:** `capture_decision` and `check_invalidation` are exposed as **Qwen-Agent custom tools** (the agent calls them itself), and the deterministic core is also served as a **real MCP server** (official SDK, stdio, keyless — `mcp_server.py`). *Verify: the Qwen agent calls the tools; an MCP client lists and calls the eight server tools.*
- **C6 — Submittable:** public, **open-source-licensed** repo + architecture diagram + ≤ 3-minute demo video + deck + written description on Devpost. *Verify: against the live Devpost rules checklist.*
- **C7 — Ambient surfacing (staged hero beat):** the user opens the 2nd-storey drawing and Trace *proactively* pops a context card — "3 decisions here, 1 pending confirmation, facade spec superseded 3 weeks ago" — with no prompt. *Verify: the card fires on the demo storyline; staged real enough to film, without building a full screen-watching daemon.* `[inference — staged for demo, see scope in docs/03]`

## 8. What this is NOT (scope guardrails)

To stay buildable in our ~9-day window (submit 7 Jul), Trace is explicitly **not**: a live BIM/IFC integration, a multi-project firm-wide knowledge base, a multi-tenant SaaS with auth, or a general-purpose contradiction detector. It is one project's decision memory, demonstrated on one deterministic storyline, done well. `[inference — see scope in docs/03]`

---

*Next:* [01 · The AEC case, strengthened →](01-aec-direction.md)
