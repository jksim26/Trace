# 00 · Project Brief — Trace

*Design-Decision Memory Agent for AEC · Qwen Cloud Hackathon, Track 1 (MemoryAgent)*
*Written 2026-06-27. Confidence tags: `[verified]` / `[web search]` / `[inference]`.*

---

## 1. The problem in one breath

On a building project, the **design brief is a living thing** — it changes across dozens of meetings as the client, architect, and consultants make decisions. But the industry records *what* was decided, not *why*. Rationale and assumptions live in email threads, half-attended meeting minutes, and people's heads — and "it's quite likely that nobody who is there at the very beginning of a project is involved at the end." `[web search — Levitt Bernstein architect, AJ roundtable]`

So three failures happen on every project:

1. **The brief silently goes stale.** A decision made in January assumes the building stays a certain way. In March, a value-engineering decision quietly contradicts that assumption — and nobody connects the two until it surfaces months later as an RFI, a clash, a change order, or a failed regulatory gateway.
2. **The "why" evaporates.** Six months later someone asks *"why the non-combustible rainscreen?"* and the answer — *"because the tower is over 15 m and SCDF Fire Code Cl 3.5.1 mandates wholly non-combustible external walls"* — is gone. The team re-litigates a settled decision, or worse, reverses it without knowing what it was protecting.
3. **There is no defensible record.** When a dispute or a safety review comes, there is no immutable, attributable trail of who decided what, when, and why.

These compound at **handover.** When a senior leaves, the rationale walks out the door with them — a clean one-to-two-month handover is rarely possible, and the incoming lead inherits live decisions with no idea what they were protecting. Because Trace captures decisions *as they are made* — consensual capture-as-you-go, never surveillance — the handover record builds itself continuously instead of being reconstructed under pressure at the end. `[inference]`

This is not a niche annoyance. It is the **information-management failure that every architecture and engineering firm actually faces**, and — uniquely for our wedge — Singapore's building law already makes a **named individual criminally accountable** for exactly the decisions this record would defend (see §4).

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
- **Secondary buyers:** the **developer / main contractor** (who carry the programme and rework cost), the **MCST / building owner** (who carries statutory duties like the Periodic Façade Inspection), and the **client/owner** who needs a defensible decision trail for disputes and claims.

## 4. Why now — the wedge that makes this mandatory, not optional

*(Framing locked 2026-07-10: **Singapore-only.** The former UK/golden-thread framing is retired — we build, demo and pitch on the home market's law. Full analysis: [07-singapore-angle.md](07-singapore-angle.md).)*

Singapore's building law already assumes this record exists — it just never built the tool:

- **A named individual is criminally accountable.** Under **Building Control Act s.9**, the design **Qualified Person** (a registered architect or professional engineer) must take all reasonable steps to ensure the works are designed to the Act and regulations, and must notify the Commissioner of any contravention they know **"or ought reasonably to know."** The duty is personal and non-delegable. `[verified — s.9 verbatim, see 07]`
- **The only prescribed record is not a defence.** Building Control Regulations **reg 22(e)** requires just "a record of all the departures or deviations relating to the structural elements" — structural-only, deviation-only, site-based, paper-era, with **no falsification detection**: nothing flags when a later decision quietly invalidates the premise an earlier one relied on. `[verified — reg 22(e) verbatim]`
- **The stakes are already on the record.** The **Toh Guan Road fire** (4 May 2017, 1 fatality) led SCDF to find **40 buildings** with potentially non-compliant cladding; the **Periodic Façade Inspection** regime (in force 1 Jan 2022: >13 m, >20 years old, every 7 years, ~30,000 buildings) and the **Fire Safety (Amendment) Act 2019** supply-chain liability followed. `[verified — see 07 §5]`

**Trace is the missing record.** In a BCA investigation or a PEB/BOA inquiry the QP must prove *what was decided, why, on what assumptions, and when.* Trace supplies an **attributable, timestamped, tamper-evident** decision memory — and its **premise-falsification alerts operationalise the s.9 "ought reasonably to know" standard** by surfacing the moment a new decision undermines a safety-critical assumption, before it becomes a defect. For APAC scale, China's **"lifelong quality responsibility"** system rests on the same principle: permanent personal accountability for the five responsible parties — a China judge already believes the premise; Trace operationalises it. This is the highest-confidence, highest-impact claim we have, and it should lead every judge-facing surface.

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
