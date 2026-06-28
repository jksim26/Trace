# Demo Script — "Maple Wharf"

**Title card:** *Maple Wharf — the decision nobody remembered making, until it nearly failed Gateway 2.*
**Runtime target:** ~3–4 minutes (fits either the 3-min or 5-min video limit).
**Setup:** the agent runs in a side panel; each scene shows a short meeting transcript on screen ([transcripts/](transcripts/)) with the agent reacting live.

---

## Title card (10 sec)

Maple Wharf is a fictional **21-storey residential building, 64 m tall**. Because it is over 18 m it is a **Higher-Risk Building (HRB)** — so the UK **Building Safety Act 2022 "golden thread"** applies: every safety decision must be **attributable to a named person, timestamped, and immutable.**

> Say it out loud: *this turns the tool from a productivity nicety into legally-required infrastructure.*

---

## SCENE 1 — CAPTURE *(RIBA Stage 2 Concept Design · 14 Jan 2026)*
*Ingests [transcripts/01-concept-design-2026-01-14.md](transcripts/01-concept-design-2026-01-14.md)*

On screen, ~6 transcript lines (architect proposes terracotta rainscreen on A2 mineral wool; fire engineer confirms combustible cladding is non-compliant over 18 m; QS notes the cost; architect says it's a compliance requirement, not a preference).

The agent silently writes a structured record and reads it back:

> **Captured D-047** — *Facade = terracotta rainscreen on A2-s1,d0 mineral wool.*
> **WHY:** HRB > 18 m; non-combustible mandated by Approved Doc B (B4).
> **WHEN:** 2026-01-14 11:42 · **WHO:** R. Wells (arch), P. Desai (fire).
> **ASSUMES:** building remains HRB; combustible cladding prohibited. · **STATUS:** valid.

**The point:** we captured the **why** and the **assumptions it rests on** — exactly what minutes, RFIs, and BIM models drop.

---

## SCENE 2 — ACTIVE INVALIDATION *(Value-Engineering workshop · RIBA Stage 4 · 3 Mar 2026)*
*Seven weeks later, different people in the room. Ingests [transcripts/02-value-engineering-2026-03-03.md](transcripts/02-value-engineering-2026-03-03.md)*

Contractor: budget's £400k over; biggest soft target is the facade — swap terracotta for an "equivalent" **aluminium composite rainscreen**, visually identical, saves ~£180k, covered under the "or equivalent" clause, no need to reopen the design.

**THE MONEY MOMENT** — before anyone agrees, the agent fires an **unprompted red INVALIDATION alert:**

> ⚠ **CONFLICT** — Proposed VE substitution (ACM rainscreen) contradicts the live premise of **D-047** (14 Jan · R. Wells / P. Desai).
> D-047's rationale: *"non-combustible mandated because building is an HRB > 18 m."* ACM is combustible — **NOT an "equivalent" under ADB B4.**
> Accepting it would (1) **breach the golden thread**, (2) require **Gateway 2 re-submission** to the Building Safety Regulator, (3) re-open the fire strategy, cavity barriers, and Part L thermal model.
> **Downstream rework:** facade support steel · fixings · fire-stopping · energy-model re-run.

Contractor: *"…I didn't know that decision existed."*

**Narration:** clash detection would only catch this when the two materials physically collide in the model — *months later, as rework*. We caught it the instant the **premise was contradicted**, in the meeting, before it became a Gateway failure.

Then show the **bi-temporal mechanic** explicitly: the agent never deletes. If the team overrides D-047, its validity is **closed** (`valid_to` set), a new decision is linked via `supersedes` / `superseded_by`, and the full "changed by whom, when, why" chain is preserved — precisely the immutable, attributable record the golden thread demands.

---

## SCENE 3 — RECALL UNDER A TIGHT CONTEXT BUDGET *(Gateway 2 dossier prep · 12 May 2026)*
*A new graduate, AL, has just joined. Ingests [transcripts/03-gateway2-prep-2026-05-12.md](transcripts/03-gateway2-prep-2026-05-12.md)*

Graduate: *"3,000 pages of minutes and 40 RFIs on this job. The Regulator wants us to evidence the facade decision. Why terracotta, and can we still change it?"*

The agent's retrieval pulls back **exactly three items** — D-047 (decision + fire rationale + named authors + date), the 3 Mar attempted ACM substitution and why it was rejected, and the ADB B4 constraint it depends on — **and explicitly nothing else.**

Show a **"context budget: 1,180 / 8,000 tokens"** meter to make the constraint visible. The agent answers in two cited sentences.

Then, to demonstrate **abstention**, AL asks: *"did we ever decide the balustrade material?"* — and the agent replies: *"No decision on record; not yet decided"* rather than hallucinating.

**Narration:** this is the Track-1 brief stated literally — *"recalling critical memories within a limited context window"* — and it's also the firm's professional-liability defence, generated in seconds instead of a paralegal-week of minute-trawling.

---

## CLOSE (15 sec)

> *"Clash detection catches two ducts hitting a beam. We catch the moment a budget decision quietly breaks a fire-safety decision someone made seven weeks ago — before it becomes an RFI, a Gateway failure, or a tragedy."*

Cut to the architecture diagram. End.

---

## Shot list / what must be on camera (maps to success criteria)

- [ ] **C1** Scene 1 — structured record read-back (capture with rationale + assumptions).
- [ ] **C2** Scene 2 — the unprompted red alert naming D-047 and explaining why (the spine).
- [ ] **C4** Scene 2 — the supersede chain (valid_to + superseded_by), never deleted.
- [ ] **C3** Scene 3 — the context-budget meter + the abstention case.
- [ ] **C5** any scene — the agent visibly calling MCP tools (`capture_decision`, `check_invalidation`, `recall_decisions`).
- [ ] Close — architecture diagram.
