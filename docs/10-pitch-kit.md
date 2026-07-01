# 10 · Pitch Kit — video script, deck, Devpost write-up

*Drafts for the three communication deliverables. Shaped by the honest self-assessment: **lead with Problem-Value** (the legal mandate), **frame the deterministic rule-pack as reliability-by-design**, and **show the Qwen/MCP sophistication** for the Technical/Innovation buckets. Storyline = Tanglin Rise (SG). Confidence tags per house style.*

---

## A. Demo video — shot-by-shot (target ≤ 3:00)

*Record `python cli.py` for the engine beats and `python bubble.py` for the ambient beat; edit to ≤ 3 min. Narration is what you say; "Screen" is what's visible.*

| Time | Screen | Narration |
|---|---|---|
| **0:00–0:18** | Title card: *"Trace — the decision nobody remembered making."* Then a split: a Jan meeting note vs a Mar one. | "On a building project, the design changes across dozens of meetings — but nobody records **why**. A cost decision in March silently breaks a fire-safety decision from January. In Singapore, the named engineer — the QP — is **personally, criminally** liable for that." |
| **0:18–0:32** | One line: *"Clash detection finds objects colliding in space. Trace finds decisions colliding across time."* | "Trace is a memory agent that catches it — the temporal analogue of clash detection." |
| **0:32–1:05** | CLI Scene 1 — the captured **D-001** card (rationale + 3 assumptions + QP names). | "Scene one: a concept-design meeting. Trace reads the transcript and captures the decision **and its reasoning** — non-combustible façade, because the building's over 15 m and SCDF Cl 3.5 mandates it. The *why* and the assumptions — exactly what minutes drop." |
| **1:05–1:50** | CLI Scene 2 — the **red invalidation alert** naming D-001 + SCDF Cl 3.5 + blast radius (incl. the QP's s.9 liability). Then the immutable-trail panel. | "Seven weeks later, a value-engineering workshop proposes a cheaper combustible panel. **Unprompted**, Trace fires: this breaks decision D-001's premise, it's non-compliant over 15 m, and it exposes the named QP to personal criminal liability. It nothing gets deleted — the rejected proposal stays on the record." |
| **1:50–2:20** | CLI Scene 3 — recall answer citing D-001/D-002 + the budget meter; then the abstention ("no decision on record"). | "Anyone can ask *why, and can we change it?* — Trace answers from only the currently-valid decisions, within a token budget, and cites them. Ask about something never decided, and it **abstains** instead of bluffing." |
| **2:20–2:40** | `mcp_tools.py` run: the agent calling `capture_decision` → `check_invalidation`. | "It's Qwen-native: the agent calls capture and invalidation as its own **MCP tools**, on Qwen Cloud." |
| **2:40–2:55** | The bubble (browser) — nudge + chat. | "And it's built to be **ambient** — *automation, not a tool*: a bubble that just tells you what's pending when you open a drawing. On-prem-capable, so nothing leaves the firm." |
| **2:55–3:00** | Close card + repo link. | "Clash detection catches ducts hitting beams. Trace catches the decision nobody remembered making — before it becomes rework, a failed submission, or a tragedy." |

**Editing notes:** keep the red alert on screen the longest (it's the money shot). Cut all loading/latency. Show real output, not slides, for scenes 1–3.

---

## B. Presentation deck — 6 slides

1. **The problem.** Hackitt's verbatim line ("*why … decisions were made … may not be recorded*") + the SG twist: the QP is personally, criminally liable but has only fragmented paper. One image: a January fire decision and a March cost decision colliding.
2. **What Trace is.** The four-part loop — capture · **active premise-invalidation** · recall-to-budget · immutable trail — and the one-liner: *temporal/semantic analogue of clash detection*.
3. **The demo.** Screenshot of the red invalidation alert (D-002 breaks D-001, SCDF Cl 3.5, QP s.9). "Unprompted, in the meeting, before rework."
4. **How it's built.** Bi-temporal decision store (never-delete supersede) → rule-pack **+** LLM → retrieve-to-budget. Qwen stack: qwen-plus extraction, MCP custom tools via Qwen-Agent, Singapore endpoint. Note: 36 tests, deterministic alert gate = reliability by design.
5. **Why we win the room.** The "empty square": AEC tools track *what's wrong in the model*; horizontal AI memory has *no AEC model*; ADRs are *manual*. Nobody ships AEC decision-graph + auto-invalidation + golden-thread-native. `[see docs/05]`
6. **Impact + roadmap.** A regulator *mandates* this data model (BSA golden thread / SG QP liability / China lifelong responsibility). Roadmap: ambient bubble, per-app integration (Revit), on-prem open-weight Qwen (data never leaves the firm).

---

## C. Devpost written description (final prose)

**Trace — a design-decision memory agent for AEC.**

**Inspiration.** In construction, the design brief evolves across dozens of meetings, but the industry records *what* was decided, not *why*. Rationale lives in email and people's heads — and "nobody who's there at the beginning of a project is involved at the end." After Grenfell, the UK made an attributable, immutable record of safety decisions **law** (the Building Safety Act "golden thread"). Singapore went further on accountability: under the Qualified Person regime, a *named* architect or engineer is **personally and criminally** liable for design decisions — yet has only fragmented, structural-only paper to defend themselves. Trace is the missing memory.

**What it does.** Trace ingests design-meeting transcripts and (1) **captures** every decision as a structured record — decision + rationale + the assumptions it rests on + author + timestamp; (2) **actively fires an alert** the moment a new decision falsifies the premise an earlier one relied on (the temporal analogue of clash detection); (3) **recalls** the currently-valid critical decisions on demand, within a token budget, and honestly abstains when nothing is on record; and (4) **never deletes** — superseded decisions are invalidated with a queryable "who changed what, when, why" trail.

**How we built it.** A bi-temporal decision store on SQLite (valid-time + transaction-time, never-delete supersession, à la Graphiti). Invalidation is a deterministic AEC rule-pack (so the alert never mis-fires) paired with an LLM premise check. Capture and recall use Qwen (qwen-plus) via function-calling on the Singapore Qwen Cloud endpoint, and the four core functions are exposed as **MCP tools through Qwen-Agent** — the agent calls them itself. 36 tests, TDD throughout.

**Challenges.** Keeping the demo's centrepiece deterministic (rule-pack-gated) so it's reliable on camera; separating *capture* (compile, don't retrieve) from *retrieval-to-budget*; and grounding the Singapore regulatory claims against primary sources (SCDF Fire Code Cl 3.5, Building Control Act s.9).

**Accomplishments.** A working four-part loop end-to-end on a real Qwen stack, an agent that calls its own MCP tools, and a problem framing a *regulator already mandates*.

**What's next.** An ambient desktop bubble ("automation, not a tool"), per-app integration (a Revit add-in), and an on-prem open-weight-Qwen deployment so nothing leaves the firm's server.

**Built with:** Qwen (qwen-plus) · Qwen-Agent / MCP · Qwen Cloud (Singapore / DashScope) · Python · SQLite. Open-source (MIT).
