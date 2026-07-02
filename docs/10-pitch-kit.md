# 10 · Pitch Kit — video script, deck, Devpost write-up

*Drafts for the three communication deliverables. Shaped by the honest self-assessment: **lead with Problem-Value** (the legal mandate), **frame the deterministic rule-pack as reliability-by-design**, and **show the Qwen-Agent tooling sophistication** for the Technical/Innovation buckets. Storyline = Tanglin Rise (SG). Confidence tags per house style.*

---

## A. Demo video — shot-by-shot (**< 3:00 — confirmed by the official rules ([doc 12](12-devpost-official-rules.md)): judges are not required to watch beyond 3:00; no copyrighted music or third-party trademarks**)

*Record `python cli.py` for the engine beats and `python bubble.py` for the ambient beat; edit to ≤ 3 min. **Open on the pain — you have ~20 seconds to make a non-construction judge feel it.** The court is the money shot. Narration is what you say; "Screen" is what's visible.*

| Time | Screen | Narration |
|---|---|---|
| **0:00–0:20** | Stark text on black: *"Grenfell, 2017 — 72 dead. Nobody could prove who decided the cladding was safe."* → *"Singapore's answer: the named engineer is personally, criminally liable."* | "After Grenfell, the UK made *losing the record of a safety decision* a crime. Singapore went further — the named engineer, the QP, is **personally, criminally liable** for every design decision. But the record he'd defend himself with? Scattered across emails and half-remembered meetings." |
| **0:20–0:32** | One line: *"Clash detection finds objects colliding in space. Trace finds decisions colliding across time."* | "Trace is the memory that fixes it — the temporal analogue of clash detection." |
| **0:32–0:58** | CLI Scene 1 — the captured **D-001** card (rationale + 3 assumptions + QP names). | "A concept-design meeting. Trace reads the transcript and captures the decision **and its reasoning** — non-combustible façade, because the building's over 15 m and SCDF Clause 3.5 mandates it. The *why*, and the assumptions — exactly what minutes drop." |
| **0:58–1:52** | CLI Scene 2 — the red alert, then **the decision court**: Proposer / Guardian / Judge → **VERDICT: REJECT** with the s.9 rationale. *(the money shot — hold it longest)* | "Seven weeks later, a value-engineering workshop proposes a cheaper — combustible — panel. Unprompted, Trace flags it. Then it convenes a **court**: three Qwen agents argue it out — the contractor's cost case, the fire-safety case citing the clause — and the **judge writes the verdict's reasoning**: rejected, and *why*, in language that stands up as the QP's legal defence. The verdict itself is **gated by the fire-code rule-pack, so it can never misfire** — reliability by design. That reasoning trail *is* the product." |
| **1:52–2:14** | CLI Scene 4 — **time-travel**: the record reconstructed as of several dates. | "Every decision carries two clocks — when it was *true*, and when we *knew* it — so Trace can **rewind**. As of the day that swap was floated, the non-combustible premise was already on record: the QP was **on notice**, and can prove it. *'What did you know, and when'* is exactly what the law asks." |
| **2:14–2:34** | CLI Scene 3 — recall (cites D-001/D-002 + budget meter) + the abstention. | "Ask *why, and can we change it?* — Trace answers from only the valid decisions, within a token budget, and cites them. Ask about something never decided — it **abstains** instead of bluffing." |
| **2:34–2:48** | `mcp_tools.py` — the agent calling `capture_decision` → `check_invalidation`. | "It's Qwen-native — the agent calls its own capture and invalidation **tools**, registered through Qwen-Agent, on Qwen Cloud." |
| **2:48–3:00** | The bubble + close card + repo link. | "Built to be **ambient** — automation, not a tool. Clash detection catches ducts hitting beams. Trace catches the decision nobody remembered making — before it becomes rework, a failed submission, or a tragedy." *(on-prem stays roadmap-only per doc 09 D5 — keep it off the demo's product claims; slide 6 carries it as roadmap)* |

**Editing notes:** the **court verdict is the money shot** — hold it longest. Cut *all* loading/latency (the court makes 3 Qwen calls — edit them out). Real output, not slides, for scenes 1–4. If you run over 3:00, drop the agent-tools beat before the court or time-travel — those two carry the Technical/Innovation score.

---

## B. Presentation deck — 6 slides

1. **The problem.** Hackitt's verbatim line ("*why … decisions were made … may not be recorded*") + the SG twist: the QP is personally, criminally liable but has only fragmented paper. One image: a January fire decision and a March cost decision colliding.
2. **What Trace is.** The four-part loop — capture · **active premise-invalidation** · recall-to-budget · never-delete trail — and the one-liner: *temporal/semantic analogue of clash detection*.
3. **The demo.** Screenshot of the red invalidation alert (D-002 breaks D-001, SCDF Cl 3.5, QP s.9). "Unprompted, in the meeting, before rework."
4. **How it's built.** Bi-temporal decision store (never-delete supersede) → deterministic rule-pack gate **+ LLM premise check over stored assumptions** → retrieve-to-budget. Qwen stack: qwen-plus extraction, the decision court's three Qwen roles (verdicts persisted), custom tools via Qwen-Agent, Singapore endpoint. Note: 63 tests, deterministic alert gate = reliability by design.
5. **Why we win the room.** The "empty square": AEC tools track *what's wrong in the model*; horizontal AI memory has *no AEC model*; ADRs are *manual*. Nobody ships AEC decision-graph + auto-invalidation + golden-thread-native. `[see docs/05]`
6. **Impact + roadmap.** A regulator *mandates* this data model (BSA golden thread / SG QP liability / China lifelong responsibility). Roadmap: ambient bubble, per-app integration (Revit), on-prem open-weight Qwen (data never leaves the firm).

---

## C. Devpost written description (final prose)

**Trace — a design-decision memory agent for AEC.**

**Inspiration.** In construction, the design brief evolves across dozens of meetings, but the industry records *what* was decided, not *why*. Rationale lives in email and people's heads — and "nobody who's there at the beginning of a project is involved at the end." After Grenfell, the UK made an attributable, immutable record of safety decisions **law** (the Building Safety Act "golden thread"). Singapore went further on accountability: under the Qualified Person regime, a *named* architect or engineer is **personally and criminally** liable for design decisions — yet has only fragmented, structural-only paper to defend themselves. Trace is the missing memory.

**What it does.** Trace ingests design-meeting transcripts and (1) **captures** every decision as a structured record — decision + rationale + the assumptions it rests on + author + timestamp; (2) **actively fires an alert** the moment a new decision falsifies the premise an earlier one relied on (the temporal analogue of clash detection); (3) **recalls** the currently-valid critical decisions on demand, within a token budget, and honestly abstains when nothing is on record; and (4) **never deletes** — superseded decisions are invalidated with a queryable "who changed what, when, why" trail.

**How we built it.** A bi-temporal decision store on SQLite (valid-time + transaction-time, never-delete supersession, à la Graphiti). Invalidation is a deterministic AEC rule-pack gate — four SCDF rules, so the alert never mis-fires — paired with an **LLM premise check** that reads each prior decision's *stored assumptions* when the rules are silent. A **decision court** of three Qwen roles argues the conflict, writes the verdict's reasoning, and persists it to the record. Capture and recall use Qwen (qwen-plus) via function-calling on the Singapore Qwen Cloud endpoint, and the four core functions are exposed as **custom tools through Qwen-Agent** — the agent calls them itself. 63 tests, TDD throughout.

**Challenges.** Keeping the demo's centrepiece deterministic (rule-pack-gated) so it's reliable on camera; separating *capture* (compile, don't retrieve) from *retrieval-to-budget*; and grounding the Singapore regulatory claims against primary sources (SCDF Fire Code Cl 3.5, Building Control Act s.9).

**Accomplishments.** A working four-part loop end-to-end on a real Qwen stack, an agent that calls its own Qwen-Agent tools, and a problem framing a *regulator already mandates*.

**What's next.** An ambient desktop bubble ("automation, not a tool"), per-app integration (a Revit add-in), and an on-prem open-weight-Qwen deployment so nothing leaves the firm's server.

**Built with:** Qwen (qwen-plus) · Qwen-Agent / MCP · Qwen Cloud (Singapore / DashScope) · Python · SQLite. Open-source (MIT).
