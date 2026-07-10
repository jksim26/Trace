# 01 · The AEC Case, Strengthened

*Why a Design-Decision Memory Agent solves a real, expensive, and now legally-mandated problem.*
*Confidence tags throughout: `[verified]` (primary source read) · `[web search]` (relayed, not independently confirmed) · `[inference]`. Treat dollar/percentage figures as **industry-reported** unless tagged `[verified]`.*

---

## 0. The thesis in one line

The AEC industry **records what was designed, but not why** — so design intent and the assumptions behind decisions are lost between phases and between people, and that loss is one of the largest, best-documented sources of rework, RFIs, disputes, and (at the extreme) safety failure in the built environment. `[web search — ITcon 2025; Hackitt 2018]`

---

## 1. The six pain points (and the evidence)

### Pain 1 — Loss of design intent / rationale between phases and into construction

The academic framing is clean. A 2025 paper in *ITcon* (Wyke et al., "Understanding Design Rationale and Intent") argues a project "must have both explicit design rationale and intent available to be successful," and that current practice **"captures what was designed but neglects why it was designed that way,"** so teams "repeat rejected alternatives and lose the reasoning behind decisions." `[web search — itcon.org/paper/2025/26]`

Worse, intent is not just forgotten — it is **actively reversed** during delivery. Architects flag the contractual **"or equivalent"** clause that lets a contractor swap a specified product for a cheaper one *even when the original was chosen for fire, thermal, or longevity performance* — the rationale evaporates because no decision trail travels with the spec. `[web search — Architects' Journal roundtable]` **This is the exact mechanism of Trace's centrepiece demo.**

### Pain 2 — The cost of rework, error, and change

The headline numbers (quote as *industry-reported*, not gospel — definitions vary by source):

| Figure | What it measures | Source / confidence |
|---|---|---|
| **~$177 B / year** | US construction labour lost to non-productive work (searching for info, conflict resolution, rework) — ~35% of workers' time | FMI / PlanGrid / Autodesk, *Construction Disconnected* 2018 `[web search]` |
| **~$31 B / year** | Of that, rework caused specifically by **miscommunication + bad/inaccessible data** ($17 B poor communication + $14.3 B poor data) | same `[web search]` |
| **48%** | Share of all jobsite rework traced to poor communication (26%) + poor project information (22%) | same `[web search]` |
| **~21% of project cost** | UK avoidable error (≈ £21 B/yr); total cost of error 10–25% | Get It Right Initiative (GIRI) `[web search]` |
| **~5% of project cost** | Direct field rework (range 2–20%) | Construction Industry Institute IR-153 `[web search]` |
| **$1.6 trillion / year** | Global productivity prize from closing construction's gap; the sector grew labour productivity ~1%/yr vs 2.8% economy-wide | McKinsey, *Reinventing Construction* 2017 `[verified — primary MGI report]` |

**The defensible, high-confidence anchors** are the McKinsey $1.6 T and the qualitative fragmentation story (Pain 4). The FMI $177 B/$31 B/48% figures are the most quotable but are reported via Autodesk/PlanGrid, not an independent primary — present them as such. `[verified — this caveat is from our own adversarial fact-check]`

### Pain 3 — Brief drift / scope creep / evolving requirements

Scope modification is repeatedly named the **single most common source of change** on projects. The brief (the contractual statement of client requirements) is rarely re-baselined or version-controlled as it evolves, so drift is detected **late** — as a change order or RFI during construction, where it is most expensive, rather than at the design stage where it is cheap to absorb. The economic law underneath: *the later a change occurs, the greater its impact.* `[web search — Designing Buildings change-control]` Reported overrun figures (≈ 28% average overrun; ~85% of projects exceed budget) trace partly to Flyvbjerg's megaproject research but circulate via vendor blogs — treat as **low confidence**. `[web search]`

### Pain 4 — Information fragmentation, tribal knowledge, people leaving

This is the emotional core, and it is exceptionally well-evidenced *from the government's own review*:

- Hackitt, *Building a Safer Future* (2018): information "is often fragmented, incomplete and held by a number of different parties, some of whom will no longer be involved once the asset has been built and handed over. **Why design and construction decisions were made, and by whom, may not be recorded.**" `[web search — gov.uk]`
- Levitt Bernstein architect Jo McCafferty: **"It's quite likely that nobody who is there at the very beginning of a project is involved at the end."** `[web search — AJ]`
- ~42% of institutional knowledge is unique to the individual who holds it and never written down. `[web search — single source, low confidence]`

This is the user's "why did we decide X?" problem, stated almost verbatim — *and a government review already validated it.*

**The headline use case — automatic handover.** When a senior architect or engineer leaves, the *why* walks out of the door with them. The textbook fix is a 1–2 month handover that, in practice, rarely happens — the departing person is already on the next job, and the receiving team inherits drawings without the reasoning. Trace attacks this at the root: because it is **there in the room** capturing every decision *and its rationale as the work happens* — ambiently, across meetings, RFIs and MOMs — the handover record is *already written* the day someone leaves. This is **consensual capture-as-you-go, not surveillance**: it records the decisions a team is already making out loud in its own forums; it does not infer or extract what an individual chose to keep private. Continuous decision-capture is what turns an impossible 1–2 month handover into an automatic one. `[inference]`

### Pain 5 — RFIs, coordination, and undocumented decisions as root cause

The Navigant Construction Forum RFI study (1,362 projects, >1 M RFIs): **~$1,080 to process a single RFI**, **~9.9 RFIs per $1 M** of project value, ~9.7 days to close, and **nearly 1 in 4 RFIs never get a reply.** `[web search]` Industry analyses attribute a large share of RFIs to design errors, incomplete drawings, or missing specs. `[web search — low confidence]` Many RFIs are **re-asks of questions that *were* answered in an earlier meeting but never written into a durable, queryable record** — exactly the loop a decision-memory layer attacks. `[inference]`

### Pain 6 — Regulation & liability (the wedge — full treatment in §2)

Design errors and omissions are a leading driver of architect/engineer professional-liability (E&O) claims (omitted fire specs, miscalculated loads), with settlements from six to seven figures. A timestamped, attributable decision trail is a direct **risk-management and legal-defence asset.** `[web search — medium/low confidence on specific shares]`

---

## 2. The QP regime — the wedge that makes Trace matter

*(Framing locked 2026-07-10: **Singapore-only**. The former UK golden-thread frame is retired from the pitch; the full Singapore analysis is in [07-singapore-angle.md](07-singapore-angle.md).)*

This is the single most powerful frame in the whole project. Lead with it.

**The chain of accountability:**
Every plan submitted to BCA goes through a **named Qualified Person** — a registered architect or professional engineer. Under **Building Control Act s.9** that individual must take all reasonable steps to ensure the works are designed to the Act and regulations, and must notify the Commissioner of any contravention they know **"or ought reasonably to know."** Personal. Non-delegable. Criminal. `[verified — s.9 verbatim, see 07]`

**What the law assumes the QP can produce** (and how it maps to our schema):

| What a defensible record needs | Trace field |
|---|---|
| Attributable to a **named person** | `author` |
| **Timestamped** — decided when, known when | `recorded_at`, `valid_from` (bi-temporal) |
| **Immutable** — historical states preserved, not overwritten | never-delete; `valid_to` + `superseded_by` chain; SHA-256 audit chain |
| Records **who decided what, when, and why** | `decision` + `author` + `valid_from` + `rationale` |
| The **premises** each decision rests on | `assumptions` — what the s.9 "ought reasonably to know" standard turns on |
| Proof the record wasn't doctored after the fact | `verify_audit_chain()` — tamper-evidence, on demand |

Yet the only record the law actually prescribes — Building Control Regulations **reg 22(e)** — is a record of "departures or deviations relating to the structural elements": structural-only, deviation-only, paper-era, with **no falsification detection** — nothing flags when a later decision quietly invalidates the premise an earlier one relied on. **That four-part gap is exactly what Trace fills.** `[verified — reg 22(e) verbatim]`

**Why this is gold for the hackathon (the 25% Problem-Value criterion):** most Track-1 entries will pitch a *nice-to-have*. Trace pitches the record a **personally, criminally liable professional** needs on the day of the inquiry — in the team's home market, and resting on a legal principle (permanent personal accountability) that China's **"lifelong quality responsibility"** system shares, so an APAC judge already believes the premise. `[inference]`

> **Honesty guardrail for the pitch:** say "no Singapore statute mandates this record" — the claim is that s.9 liability *assumes* the QP can produce it, not that it is prescribed. The absence is the gap, and the gap is the product.

---

## 3. How AEC actually works (so the product is credible)

The agent must speak the industry's language. The essentials:

**Design runs through gated stages**, each ending in a defined "Information Exchange" that freezes the current design and hands it on:
- **UK — RIBA Plan of Work**, stages 0–7: 0 Strategic Definition · 1 Preparation & Briefing · 2 Concept Design · 3 Spatial Coordination · 4 Technical Design · 5 Manufacturing & Construction · 6 Handover · 7 Use. `[web search — RIBA]`
- **US — AIA phases:** Schematic Design (SD) → Design Development (DD) → Construction Documents (CD) → Bidding → Construction Administration (CA). The owner formally signs off at the end of SD and DD. `[web search — AIA]`

**The brief is the spine.** It starts as a *Strategic Brief* (Stage 0), becomes the *Project Brief* (Stage 1), is **frozen as a baseline at end of Concept/SD** (after which *change control* applies), and decomposes into the **Schedule of Accommodation / Area Schedule** (→ GIA/NIA efficiency, a core financial KPI), **Room Data Sheets (RDS)**, **Design Criteria**, and **performance vs prescriptive specifications**. `[web search — Designing Buildings]`

**Where decisions get lost** (the three cruellest transitions): `[web search + inference]`
1. The **Concept → Coordination brief freeze** — the frozen brief and the evolving drawings diverge silently; assumptions ("plant on roof", "naturally ventilated") never logged.
2. The **planning pause (RIBA 3 → 4)** — decisions made to *win planning* (heights, materials, parking) become binding conditions that later teams forget are binding.
3. The **design → construction handover (4 → 5)** — new parties join and "work from their interpretation of the drawings rather than the documented rationale."

**The decisions live scattered** across: meeting minutes / design review records, **RFIs** (ask, authorise nothing), **Change Orders** (signed, amend the contract), **CCDs**, **Design Change Notices**, **Value-Engineering logs**, **derogations/concessions** (approved deviations from spec), **NCRs**, and **transmittals**. `[web search]`

**Critical gap = there is no AEC-standard "design decision log."** Software has the formalised **Architecture Decision Record (ADR)**; AEC has only the *generic* PM "decision log/register," applied inconsistently, with rationale routinely vaporising into email and verbal agreement. **That missing standard is the product opportunity.** `[web search + inference]`

**The information backbone is standardised** (position Trace as *complementary*, not competing): **ISO 19650** governs information management (EIR → BEP → MIDP/TIDP, all in a **Common Data Environment** with WIP → Shared → Published → Archived states). Note: ISO 19650 centres on information *requirements and exchanges*, **not decisions per se** — which is exactly the layer Trace adds on top. `[web search — ISO 19650]`

---

## 4. Four worked examples — a decision changes, and what it makes obsolete

These are the demo fuel. In each, the model eventually updates — but the *decision + rationale + the list of now-invalid downstream items* is what no current tool reliably holds. And holding it is only half the job: the differentiator is that Trace **pushes** the invalidation the moment the triggering decision lands — *automation, not a tool you have to remember to query*. `[inference from sourced cascade material; an AEC reader will recognise these as realistic]`

### A — Parking count 200 → 150 (budget / revised transport statement) · *RIBA 2–3*
Invalidates: basement parking layout (possibly deletes a whole basement level); ramp geometry, cycle store (planning often demands *more* cycle spaces in exchange); **structural** foundations/retaining walls if a level goes; **MEP** car-park ventilation & EV-charging counts; **fire** smoke-extract strategy; **QS** GIA → area schedule → cost plan → appraisal; **planning** transport-statement condition → *re-approval risk*.

### B — Facade material change (mineral rainscreen → PE-core ACP, or combustible → non-combustible) · *RIBA 4* — **the demo centrepiece**
Invalidates: **structural** dead load → support steel/brackets, slab-edge, fixings (wind load re-check); **fire** combustibility rating (SCDF Fire Code Cl 3.5.1: wholly non-combustible over 15 m; Cl 3.15.13 ACP core), cavity barriers, fire-stopping → **fire-safety plan re-approval** + the named QP's s.9 exposure; **building physics** U-value, condensation, energy model re-run; **architecture** setting-out, reveals, window schedule; **QS/programme** cost (cladding ≈ 1.5–2×), new specialist package, lead times, warranties.

### C — Floor-to-floor height change (3.6 m → 4.0 m for services, or reduced to meet a height cap) · *RIBA 3*
Invalidates: **planning** overall height → massing, daylight/sunlight, height condition → *re-approval risk* (if total height is capped, a whole floor may be lost); **brief/finance** lost floor → NIA → appraisal; **structural** column lengths, stability, core/stairs; **architecture/Regs** stair riser count (Part K), lift travel/shaft; **facade** panel module, extra row → cost; **MEP** riser heights, duct drops, ceiling-void re-coordination.

### D — Core relocation (move lifts/stairs/risers to improve lettable floorplate) · *RIBA 2–3* — highest single-decision blast radius
Invalidates: **structural** the core *is* the lateral-stability system → stability re-design, transfer structure if it no longer stacks; **brief/finance** floorplate efficiency, NIA/GIA, lettable area → the financial model (the very reason for the move must be re-proven); **MEP** all vertical risers re-routed; **fire** escape routes, travel distances, firefighting shaft, pressurisation → fire-code re-check (SCDF Ch 2/4); **architecture/Regs** lift strategy, accessibility (BCA Code on Accessibility), every floor's RDS.

---

## 5. Glossary the agent (and pitch) must get right

RIBA Plan of Work · AIA phases (SD/DD/CD/CA) · Information Exchange · Project Brief / Employer's Requirements (ER) · Schedule of Accommodation · GIA / NIA / net-to-gross efficiency · Room Data Sheet (RDS) · performance vs prescriptive spec · design freeze / baseline · change control · **RFI** · Change Order / Variation · CCD · Design Change Notice · Value Engineering (VE) · **derogation / concession** · NCR · transmittal · **Decision Log / ADR** · **ISO 19650** · EIR · BEP · MIDP/TIDP · **CDE** (WIP/Shared/Published/Archived) · **QP** (Qualified Person — Building Control Act s.9) · **SCDF Fire Code** (Cl 3.5.1 non-combustible > 15 m; Cl 3.15.13 ACP core) · **PFI** (Periodic Façade Inspection: >13 m, >20 yrs, every 7 yrs, Competent Person) · **CORENET X** / **IDD** · clash detection (hard/soft/time) · A1 / A2-s1,d0 / Class 0 (non-combustible fire ratings).

---

## 6. What to verify before quoting numbers to a judge

- HIGH confidence: Building Control Act s.9 + reg 22(e) (verbatim, primary source); SCDF Cl 3.5 (>15 m); PFI regime facts; Toh Guan Road (40 buildings); McKinsey $1.6 T; the fragmentation/personnel-churn narrative. **Lead with these.**
- MEDIUM: FMI $177 B/$31 B/48% (reported via Autodesk, primary PDF not opened); CII ~5%; GIRI ~21%; Navigant RFI figures; the ITcon "what not why" finding. **Present as "industry-reported."**
- LOW: scope-creep overrun %s; "70% of RFIs from design errors"; tribal-knowledge 42%/70%. **Use sparingly, hedge.**

---

*Next:* [02 · Architecture & Framework →](02-architecture.md)
