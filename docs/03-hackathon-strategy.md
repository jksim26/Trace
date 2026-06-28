# 03 · Hackathon Strategy — How Trace Wins Track 1

*Confidence tags: `[verified]` (read across ≥2 sources / primary) · `[web search]` · `[inference]`. The official Devpost rules page renders empty to automated fetch — items marked **VERIFY LIVE** must be confirmed on the page before the deadline.*

---

## 1. The event, in facts

| Field | Value | Confidence |
|---|---|---|
| Name | **Global AI Hackathon Series with Qwen Cloud** (Alibaba Cloud, on Devpost) | `[verified]` |
| Format | 100% online, global; 5 tracks ("arenas") | `[verified]` |
| Our track | **Track 1 — MemoryAgent** | `[verified]` |
| Launch | ~26 May 2026 | `[web search]` |
| **Hard submission deadline** | **9 July 2026, 14:00 PDT** (= 10 July 02:30 IST; Alibaba's tweet rounds to "8 July") | `[verified — timezone-checked]` |
| **★ Our internal submission target** | **7 July 2026** — submit 2 days early; keep 8–9 Jul as contingency buffer | team decision |
| Judging | ~10–30 July 2026 | `[web search — single source]` |
| Winners | ~7 August 2026 | `[web search — single source]` |
| Prize / track | **$10,000** = $7,000 cash + $3,000 cloud credits, ×5 track winners | `[verified]` |
| Extra awards | 10× Blog Post ($500+$500) + 10× Honorable Mention ($500+$500); total pool **$70,000+** | `[verified]` |
| Team size | **1–5 members** | `[verified]` |
| Build budget | **$40 coupon/participant** + Model Studio new-user free quota (~1M free tokens/model, Singapore, ~90 days) | `[web search]` |

**Today is 2026-06-28. We're targeting submission by 7 July (≈9 days of build), leaving 8–9 July as buffer before the hard 9 Jul 14:00 PDT deadline.** Plan accordingly (§6).

## 2. The five tracks (for context; we are Track 1)

1. **MemoryAgent** — persistent memory; storage/retrieval, timely forgetting, recall under limited context. ← **us**
2. AI Showrunner — video-gen pipeline (Wan / HappyHorse).
3. **Agent Society** — multi-agent collaboration/negotiation with measurable gain vs single-agent. ← *this was your deferred Idea B; confirmed Track 3.*
4. Autopilot Agent — end-to-end business-workflow automation, production-ready, human-in-the-loop.
5. EdgeAgent — Qwen on physical/IoT devices.

## 3. Judging criteria — and how we max each `[verified weights; descriptions partly conflict, see ⚠]`

> **🇸🇬 Singapore note (added 2026-06-28):** The Problem-Value row below leads on the UK golden thread. For your Singapore team + Alibaba/Qwen judges, the recommended re-lead is **Singapore QP personal liability → China lifelong quality responsibility → UK golden thread (one line)**, tied to **CORENET X / IDD 70%-by-2025**. This protects you from the "UK isn't your market" reaction. See **[07-singapore-angle.md](07-singapore-angle.md) §2**.

| Criterion | Weight | How Trace scores |
|---|---|---|
| **Technical Depth & Engineering** | **30%** | Bi-temporal decision graph with explicit edge-invalidation (valid_from/valid_to/recorded_at/superseded_by, never delete); LLM contradiction pass narrowed by semantic similarity; hybrid retrieval (text-embedding-v4 + BM25 + qwen3-rerank) with retrieve-to-budget; clean modular code + architecture diagram. |
| **Innovation & AI Creativity** | **30%** | The **AEC decision-dependency graph + active premise-invalidation** as a category-defining idea; PLUS sophisticated Qwen use — native function-calling, **MCP custom tools/skills via Qwen-Agent**, qwen3.7-max 1M context, context caching. |
| **Problem Value & Impact** | **25%** | Lead with the **statutory golden thread** (BSA 2022 + Hackitt's verbatim quote), then industry-reported pain numbers. Reframe the product as *mandatory* for HRBs and a professional-liability defence globally — the strongest impact story any Track-1 entrant is likely to have. |
| **Presentation & Documentation** | **15%** | The 3-scene transcript demo with the on-screen **red invalidation alert** and **context-budget meter** "visualises key logic effectively" exactly as the rubric asks; crisp README + architecture diagram + OSS-licensed repo. |

> **⚠ Known ambiguity (from our adversarial fact-check):** sources disagree on which 30% bucket owns the "sophisticated Qwen API / MCP use" description vs the "architecture / code quality" description. The labels and weights (30/30/25/15) are solid; the description↔label pairing is not. **Mitigation: build to BOTH descriptions** — ship strong architecture/code quality *and* sophisticated Qwen API/MCP use — so the score holds regardless. `[verified — direct source conflict]`

## 4. The differentiation (one paragraph, memorise it)

No competitor closes the four-part loop of **decision + rationale + timestamp + active downstream invalidation.** AEC incumbents (Revizto, Newforma Konekt, BIMcollab, Autodesk Construction Cloud, Aconex, Procore) track issues/clashes/documents with audit trails but store *what* is wrong in the model, never *why* a choice was made or whether it still holds. AEC AI startups (Helonic, Drawer AI, Togal) do forward, point-in-time error detection on a drawing set, not longitudinal decision memory. The closest analogue — software **ADRs** — captures decision + rationale + a superseded-by link, but supersession is a *manual* status flip, software-only, with no automatic detection. Horizontal AI memory (Supermemory, Mem0/Zep) and KB contradiction-detectors (Alhena, Fini) already handle abstract contradictions — *so "we detect conflicts" is NOT itself novel; say so on stage to stay credible.* The defensible wedge is the combination nobody ships: an **AEC-domain decision-dependency graph** that performs **active premise-invalidation** and is **golden-thread native** (attributable, timestamped, immutable). Full table: [05-competitive-landscape.md](05-competitive-landscape.md).

## 5. Submission deliverables checklist `[verified unless noted]`

- [ ] **Public GitHub repo** — must be public **AND open source with a license file**. `[verified — stronger than "just public"]`
- [ ] **Demo video** — public on YouTube/Vimeo/Youku, link on the form. **Length: edit to ≤ 3 min** (sources conflict 3 vs 5 min → the tight cut satisfies either). **VERIFY LIVE.**
- [ ] **Architecture diagram** (turn the §8 text diagram in [02](02-architecture.md) into a clean visual).
- [ ] **Presentation deck**.
- [ ] **Written project description** on Devpost.
- [ ] Project **uses Qwen models on Qwen Cloud** (required to qualify). `[verified]`
- [ ] *(Insurance)* deployed on an Alibaba Cloud instance — a web-search summary suggests deployment may be required; unconfirmed. **VERIFY LIVE**; deploy as insurance regardless. `[web search — unverified]`

> **Good news from the fact-check:** pre-existing projects are allowed *if significantly updated after the submission period starts* — so starting to build now and iterating is fine; it does not have to be a from-scratch-during-the-window build. `[verified — Devpost rules snippet]` Originality still required (no direct copying of OSS projects); teams retain IP, grant the sponsor a non-exclusive license for judging/promo. `[verified]`

## 6. The build plan (today = 28 Jun · internal submit = **7 Jul** · hard deadline = 9 Jul 14:00 PDT)

*Compressed to land submission on 7 July, leaving 8–9 Jul as pure contingency. Repo + OSS license are already ✅ done.*

| Days | Goal | Verify |
|---|---|---|
| **28–29 Jun** | Qwen Cloud account, $40 coupon, Singapore endpoint smoke-test; decision schema + SQLite store + never-delete supersede. **Confirm live Devpost rules** (video length, deployment clause, video host). | First qwen3.7-max call returns; a Decision row round-trips. |
| **30 Jun–1 Jul** | `capture_decision` (extraction) + `check_invalidation` (rule-pack + LLM) → the **push alert** works on the demo transcripts. | C1 + C2 fire reliably on the storyline. |
| **2–3 Jul** | Hybrid retrieve + composite re-score + retrieve-to-budget + abstention + **context-budget meter**; audit/history view. | C3 + C4 demonstrable on camera. |
| **4 Jul** | Wrap as **Qwen-Agent MCP tools**; thin UI/CLI for filming; (insurance) deploy to Alibaba Cloud. | C5 works; app runs on the cloud instance. |
| **5–6 Jul** | Record + edit ≤3-min video; architecture diagram; deck; README; written description. | All §5 boxes ticked. |
| **★ 7 Jul** | **SUBMIT on Devpost (internal target).** Flip repo to public. | Submission confirmed; links public; repo public + OSS-licensed. |
| **8–9 Jul** | **Buffer** — fixes, re-record, polish if needed; final check before the hard 9 Jul 14:00 PDT deadline. | Nothing left to chance. |

**Risk-driven sequencing:** the invalidation alert (C2) is the demo's spine — build it *second*, right after the store, so if time runs short everything after it is polish, not core. With only ~9 build days for 2 people, protect C1–C3 ruthlessly and treat every stretch item as optional.

## 7. Top risks & mitigations `[from synthesis]`

| Risk | Mitigation |
|---|---|
| LLM contradiction detection mis-fires live (false +/-) | Hard-code one deterministic storyline; gate the demo alert on the **rule-pack**, not pure LLM judgement. |
| Demo-video length rule unresolved (3 vs 5 min) | Edit to ~3 min; **verify live** before upload. |
| Judging 30%-description swap | **Build to both** 30% descriptions. |
| Possible Alibaba-deployment requirement | Verify live; **deploy to Alibaba Cloud as insurance.** |
| $40 coupon may not cover embeddings/rerank/caching; qwen3.7-max SG pricing unannounced at launch | Default to qwen-plus/flash for routine extraction; reserve qwen3.7-max for contradiction reasoning; stack the per-model free quota; keep everything on the Singapore endpoint. |
| Over-scoping the graph DB / eval harness | Freeze the MVP four-part loop on **SQLite** first; graph viz / sleep-time / eval = strictly post-MVP. |
| A sharp judge: "ADRs already do superseded; KB tools already detect contradictions" | **Pre-empt it on stage** — concede generic contradiction detection exists, then claim the defensible *combination* (AEC dependency graph + auto invalidation + rationale + golden-thread native). |
| Cost stats are mostly medium/low-confidence | Anchor impact on the **high-confidence** items (Hackitt quote, BSA statute, McKinsey $1.6T); present rework figures as "industry-reported." |

## 8. The seven strategic moves (the synthesis, distilled)

1. Make **"active premise-invalidation on an AEC decision-dependency graph"** the entire identity — it's the one thing no competitor ships and it photographs beautifully as the red alert.
2. Lead every judge-facing surface with the **golden-thread / BSA-2022 statutory wedge** — highest confidence, highest impact, maximises the 25% bucket.
3. **Bank the MCP/custom-skills hook concretely** — implement `capture_decision` + `check_invalidation` as Qwen-Agent MCP tools; build to both 30% descriptions.
4. Ship the **four-part loop on SQLite first**; resist the graph-DB/eval-harness temptation until the demo is filmable.
5. **Hard-code one deterministic storyline** with a tiny HRB/ADB rule-pack so the centrepiece never misfires.
6. **Stay honest** on novelty and statistics — a credible team scores higher than an overclaiming one.
7. **Before the deadline:** verify video length + deployment clause on the live page; confirm repo is public *with* an OSS license; keep inference on the Singapore endpoint; deploy to Alibaba as insurance.

---

*Next:* [04 · Qwen Tech Reference →](04-qwen-tech-reference.md) · [05 · Competitive Landscape →](05-competitive-landscape.md) · [06 · Open Questions →](06-open-questions.md)
