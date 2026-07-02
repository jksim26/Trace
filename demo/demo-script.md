# Demo Script — "Tanglin Rise"

**Title card:** *Tanglin Rise — the decision nobody remembered making, until it nearly exposed the QP.*
**Runtime target:** **< 3 minutes** — confirmed by the live rules read 2026-07-02: "Judges are not required to watch beyond three minutes" ([docs/12](../docs/12-devpost-official-rules.md)).
**Setup:** the agent runs in a side panel; each scene shows a short meeting transcript on screen ([transcripts/](transcripts/)) with the agent reacting live.

---

## Title card (10 sec)

Tanglin Rise is a fictional **28-storey residential condominium, 95 m tall**, in Singapore. Because it exceeds **15 m**, **SCDF Fire Code 2023 Cl 3.5** requires its external walls to be **wholly non-combustible** `[verified — Cl 3.5; use 15 m]`. And under **Building Control Act s.9**, the design **QP** — a *named individual* architect — carries **personal, non-delegable, criminal** accountability for that compliance `[verified — s.9 due-diligence duty]`. Yet the law gives that QP only **fragmented, structural-only, paper-era records** (Building Control Regs reg 22) to defend themselves with.

> Say it out loud: *Singapore didn't legislate a "golden thread" — it made an individual personally and criminally liable. Trace is the attributable, immutable decision memory the law already assumes that QP can produce.*

---

## SCENE 1 — CAPTURE *(Concept Design · 14 Jan 2026)*
*Ingests [transcripts/01-concept-design-2026-01-14.md](transcripts/01-concept-design-2026-01-14.md)*

On screen, ~6 transcript lines (the architect — the design QP — specifies a non-combustible mineral rainscreen; the fire engineer confirms combustible cladding is non-compliant over 15 m and wants it minuted; the QS notes the premium; the architect says it's a compliance requirement, not a preference, and that it's their name and s.9 duty on the line).

The agent silently writes a structured record and reads it back:

> **Captured D-001** — *Façade = non-combustible mineral rainscreen (A1 mineral-core panels; Class 0 outer layers per Cl 3.15).*
> **WHY:** building 95 m (> 15 m); wholly non-combustible external wall mandated by SCDF Fire Code 2023 Cl 3.5.
> **WHEN:** 2026-01-14 11:42 · **WHO:** K. Lim (design QP / architect), M. Ong (fire).
> **QP LIABLE:** K. Lim — personal due-diligence duty, Building Control Act s.9.
> **ASSUMES:** building remains > 15 m; combustible external cladding prohibited. · **STATUS:** valid.

**The point:** we captured the **why**, the **assumptions it rests on**, and **whose name is on it** — exactly what minutes, RFIs, and BIM models drop.

---

## SCENE 2 — ACTIVE INVALIDATION *(Value-Engineering workshop · 3 Mar 2026)*
*Seven weeks later, different people in the room — and the fire engineer is not one of them. Ingests [transcripts/02-value-engineering-2026-03-03.md](transcripts/02-value-engineering-2026-03-03.md)*

Contractor: the cost plan's over budget; the biggest soft target is the façade — swap the non-combustible mineral rainscreen for an "equivalent" **polyethylene-core aluminium composite panel (PE-core ACP)**, visually identical, the biggest single saving on the package, covered under the "or equivalent" clause, no need to reopen the design.

**THE MONEY MOMENT** — before anyone agrees, the agent fires an **unprompted red INVALIDATION alert:**

> ⚠ **CONFLICT** — Proposed VE substitution **D-002** (PE-core ACP) contradicts the live premise of **D-001** (14 Jan · K. Lim / M. Ong).
> D-001's rationale: *"wholly non-combustible mandated because building exceeds 15 m."* A PE core is combustible — **NOT an "equivalent" under SCDF Fire Code Cl 3.5.**
> Accepting it would (1) render the external wall **non-compliant over 15 m**, (2) expose the **named QP (K. Lim) to personal criminal liability under Building Control Act s.9**, (3) require **re-submission of the fire-safety plan to SCDF**, and (4) fail the recurring **Periodic Façade Inspection** `[verified — PFI regime]`.
> **Real-world echo:** the **Toh Guan Road fire (4 May 2017, 1 fatality)**, where visually similar compliant and PE-core panels were mixed; SCDF later found **40 buildings** with potentially non-compliant cladding `[verified — 40 buildings; preceded Grenfell]`.
> **Downstream rework:** façade support steel · fixings · fire-stopping · fire-engineering re-approval.

Contractor: *"…I didn't know that decision existed."*

**Narration:** clash detection would only catch this when two materials physically collide in the model — *months later, as rework*. We caught it the instant the **premise was contradicted**, in the meeting, before it became a submission failure — or a fire.

Then show the **never-delete trail** explicitly: the agent never deletes. **D-002** is preserved on the record as a **rejected** proposal alongside the live decision it challenged (**D-001**) — the "we considered a cheaper panel and rejected it, and why" trail survives. Had the team instead **overridden** D-001, `supersede_decision` would close its validity (`valid_to` set), link the replacement via `superseded_by`, and preserve the full "changed by whom, when, why" chain *(built and tested; not shown in this storyline, where the proposal is rejected)* — precisely the attributable, never-delete record a personally-liable QP needs to stand behind a s.9 due-diligence defence.

---

## SCENE 3 — RECALL UNDER A TIGHT CONTEXT BUDGET *(Handover / BCA + SCDF submission prep · 12 May 2026)*
*A new joiner, AM, has just picked up the façade package. Ingests [transcripts/03-recall-handover-2026-05-12.md](transcripts/03-recall-handover-2026-05-12.md)*

New joiner: *"3,000 pages of minutes and 40 RFIs on this job. The authorities want the basis for the façade decision evidenced. Why the non-combustible rainscreen, and can we still change it?"*

The agent's retrieval pulls back **exactly three items** — D-001 (decision + fire rationale + named QP + date), the 3 Mar attempted PE-core ACP substitution (D-002) and why it was rejected, and the Cl 3.5 constraint it depends on — **and explicitly nothing else.**

Show a **"context budget: 1,180 / 8,000 tokens"** meter to make the constraint visible. The agent answers in two cited sentences.

Then, to demonstrate **abstention**, AM asks: *"did we ever decide the sky-terrace planter/balustrade material?"* — and the agent replies: *"No decision on record; not yet decided"* rather than hallucinating.

**Narration:** this is the Track-1 brief stated literally — *"recalling critical memories within a limited context window"* — and it's also the QP's professional-liability defence and a clean handover: because the s.9 duty attaches to a *named* individual, the successor inherits a live, defensible decision record instead of reconstructing it from a paralegal-week of minute-trawling.

---

## CLOSE (15 sec)

> *"Clash detection catches two ducts hitting a beam. We catch the moment a budget decision quietly breaks a fire-safety decision someone made seven weeks ago — before it becomes an RFI, a failed submission, a personally-liable QP, or a tragedy. The UK criminalised losing this record after Grenfell; in Singapore the QP is already personally liable — Trace is the defensible decision memory the law assumes they can produce."* `[verified — Grenfell 14 Jun 2017]`

Cut to the architecture diagram. End.

---

## Shot list / what must be on camera (maps to success criteria)

- [ ] **C1** Scene 1 — structured record read-back (capture with rationale + assumptions + named QP).
- [ ] **C2** Scene 2 — the unprompted red alert naming D-001 and explaining why (the spine).
- [ ] **C4** Scene 2 — the never-delete trail: D-002 preserved as a rejected proposal, nothing erased.
- [ ] **C3** Scene 3 — the context-budget meter + the abstention case.
- [ ] **C5** any scene — the agent visibly calling its Qwen-Agent tools (`capture_decision`, `check_invalidation`, `recall_decisions`).
- [ ] Close — architecture diagram.
