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

**Today is 2026-06-30. We're targeting submission by 7 July (≈7 days of build), leaving 8–9 July as buffer before the hard 9 Jul 14:00 PDT deadline.** Plan accordingly (§6).

## 2. The five tracks (for context; we are Track 1)

1. **MemoryAgent** — persistent memory; storage/retrieval, timely forgetting, recall under limited context. ← **us**
2. AI Showrunner — video-gen pipeline (Wan / HappyHorse).
3. **Agent Society** — multi-agent collaboration/negotiation with measurable gain vs single-agent. ← *this was your deferred Idea B; confirmed Track 3.*
4. Autopilot Agent — end-to-end business-workflow automation, production-ready, human-in-the-loop.
5. EdgeAgent — Qwen on physical/IoT devices.

## 3. Judging criteria — and how we max each `[verified weights; descriptions partly conflict, see ⚠]`

> **🇸🇬 Framing locked (2026-07-10): Singapore-only.** The pitch leads **Singapore QP personal liability → China lifelong quality responsibility**, tied to **CORENET X / IDD 70%-by-2025**. The former UK golden-thread frame is retired everywhere. See **[07-singapore-angle.md](07-singapore-angle.md) §2**.

| Criterion | Weight | How Trace scores |
|---|---|---|
| **Technical Depth & Engineering** | **30%** | Bi-temporal decision graph with explicit edge-invalidation (valid_from/valid_to/recorded_at/superseded_by, never delete); LLM contradiction pass narrowed by semantic similarity; hybrid retrieval (text-embedding-v4 + BM25 + qwen3-rerank) with retrieve-to-budget; clean modular code + architecture diagram. |
| **Innovation & AI Creativity** | **30%** | The **AEC decision-dependency graph + active premise-invalidation** as a category-defining idea; PLUS sophisticated Qwen use — native function-calling, **MCP custom tools/skills via Qwen-Agent**, qwen3.7-max 1M context, context caching. |
| **Problem Value & Impact** | **25%** | Lead with **QP personal criminal liability** (Building Control Act s.9, verbatim) against the reg 22(e) paper-record gap, anchored by the **Toh Guan Road fire → 40 buildings → PFI regime** chain, then industry-reported pain numbers. Reframe the product as the record the law already *assumes* a liable professional can produce — the strongest impact story any Track-1 entrant is likely to have. |
| **Presentation & Documentation** | **15%** | The 3-scene transcript demo with the on-screen **red invalidation alert** and **context-budget meter** "visualises key logic effectively" exactly as the rubric asks; crisp README + architecture diagram + OSS-licensed repo. |

> **✅ Ambiguity RESOLVED (live rules read, 2026-07-02 — see [12-devpost-official-rules.md](12-devpost-official-rules.md)):** "Sophisticated use of Qwen Cloud APIs — e.g., custom skills, MCP integrations" + "algorithm/engineering innovation" own **Innovation & AI Creativity (30%)**; "architecture quality, engineering excellence, tech stack sophistication" own **Technical Depth & Engineering (30%)**. Building to both remains the right play. Also confirmed: **Stage One is a pass/fail gate** — the project must "reasonably fit the theme and reasonably apply the required APIs/SDKs" before weighted judging begins. `[verified — rules §6]`

## 4. The differentiation (one paragraph, memorise it)

No competitor closes the four-part loop of **decision + rationale + timestamp + active downstream invalidation.** AEC incumbents (Revizto, Newforma Konekt, BIMcollab, Autodesk Construction Cloud, Aconex, Procore) track issues/clashes/documents with audit trails but store *what* is wrong in the model, never *why* a choice was made or whether it still holds. AEC AI startups (Helonic, Drawer AI, Togal) do forward, point-in-time error detection on a drawing set, not longitudinal decision memory. The closest analogue — software **ADRs** — captures decision + rationale + a superseded-by link, but supersession is a *manual* status flip, software-only, with no automatic detection. Horizontal AI memory (Supermemory, Mem0/Zep) and KB contradiction-detectors (Alhena, Fini) already handle abstract contradictions — *so "we detect conflicts" is NOT itself novel; say so on stage to stay credible.* The defensible wedge is the combination nobody ships: an **AEC-domain decision-dependency graph** that performs **active premise-invalidation** on an **attributable, timestamped, tamper-evident** record. And the *delivery* is part of the wedge: Trace is **automation, not a tool** — it runs ambiently and **pushes** the alert into context the moment a premise breaks, instead of waiting to be opened and queried; this **active push, not passive pull** is what doc 05 calls the single sharpest differentiator. Full table: [05-competitive-landscape.md](05-competitive-landscape.md).

> **On-prem = the security moat (roadmap, not a demo claim):** the hackathon **requires hosted Qwen Cloud** (Singapore DashScope endpoint), so for the 7-July demo, data does leave to Alibaba Cloud. But the product can run on **open-weight Qwen on-prem / air-gapped** — nothing leaves the firm's server — which SaaS incumbents (Glean, Microsoft 365 Copilot) structurally cannot match. Caveat: the flagship **qwen3.7-max is API-only**, so an on-prem build would run a smaller open-weight Qwen. `[web search / general knowledge — not independently verified]`

## 5. Submission deliverables checklist `[verified unless noted]`

*(All items below confirmed against the live rules, 2026-07-02 — verbatim in [12-devpost-official-rules.md](12-devpost-official-rules.md).)*

- [ ] **Public GitHub repo** — public **AND open source with a license file**, and the license must be "detectable and visible at the top of the repository page (in the About section)"; repo must contain all source, assets, and working instructions. `[verified — rules §4]`
- [ ] **Demo video** — public on YouTube/Vimeo/Youku, link on the form. **Length: < 3 min** ("Judges are not required to watch beyond three minutes"). No third-party trademarks or copyrighted music. `[verified — rules §4]`
- [ ] **Architecture diagram** — required: "a clear visual representation of your system (e.g., how Qwen Cloud connects to your backend, database, and frontend)" (turn the §8 text diagram in [02](02-architecture.md) into a clean visual). `[verified — rules §4]`
- [ ] **Presentation deck**.
- [ ] **Written project description** on Devpost — include the "significantly updated during the Submission Period" explanation. `[verified — rules §4]`
- [ ] Project **uses Qwen models on Qwen Cloud** (required to qualify; also the Stage One pass/fail gate). `[verified]`
- [ ] **MANDATORY: Proof of Alibaba Cloud Deployment** — "You must demonstrate that the backend is running on Alibaba Cloud. Proof must be a link to a code file in their code repo that demonstrates use of Alibaba Cloud services and APIs." Deploy the backend AND link the code file. `[verified — rules §4; upgraded from "insurance"]`
- [ ] **Testing access link** — "a link to a website, functioning demo, or a test build," free access through 31 Jul (the deployed instance doubles as this). `[verified — rules §4]`
- [ ] *(Optional)* **Blog Post bonus prize** — public blog/social post on the build journey, link in the submission (10 × $500 + $500 pool). `[verified — rules §4/§8]`

> **Good news from the fact-check:** pre-existing projects are allowed *if significantly updated after the submission period starts* — so starting to build now and iterating is fine; it does not have to be a from-scratch-during-the-window build. `[verified — Devpost rules snippet]` Originality still required (no direct copying of OSS projects); teams retain IP, grant the sponsor a non-exclusive license for judging/promo. `[verified]`

## 6. The build plan (drafted 28 Jun · internal submit = **7 Jul** · hard deadline = 9 Jul 14:00 PDT)

*Compressed to land submission on 7 July, leaving 8–9 Jul as pure contingency. Repo + OSS license are already ✅ done.*

> **⏱ Status update (2026-06-30):** today is now **30 Jun**, not 28 Jun — the table's "28 Jun" anchor below is kept as-is for reference. We're on the **foundation spine** (decision schema + SQLite never-delete store, the 28–29 Jun row), which is the **current step**; the 30 Jun–1 Jul capture + invalidation-alert row is next. `[team status]`

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

> **Demo scope — build for real vs. stage (the 7-July cut):** **BUILD FOR REAL** the full four-part loop end to end (**C1–C4**) — **capture → invalidate (+ push alert) → recall-to-budget → audit** — on the one deterministic storyline. **STAGE one ambient "hero" moment:** the user opens the 2nd-storey drawing and Trace pops *"3 decisions here · 1 pending confirmation · facade spec superseded 3 weeks ago"* — real enough to film without building a full screen-watching daemon. The staged moment sells **"automation, not a tool"**; the real four-part loop proves it. `[team decision]`

## 7. Top risks & mitigations `[from synthesis]`

| Risk | Mitigation |
|---|---|
| LLM contradiction detection mis-fires live (false +/-) | Hard-code one deterministic storyline; gate the demo alert on the **rule-pack**, not pure LLM judgement. |
| ~~Demo-video length rule unresolved~~ **RESOLVED: < 3 min** | Edit to < 3:00; judges won't watch beyond it. `[verified — rules §4]` |
| ~~Judging 30%-description swap~~ **RESOLVED** | MCP/custom-skills = Innovation 30%; architecture/code = Technical 30%. Build to both anyway. `[verified — rules §6]` |
| ~~Possible~~ **CONFIRMED Alibaba-deployment requirement** | **Mandatory:** deploy the backend on Alibaba Cloud + link a repo code file demonstrating Alibaba Cloud services/APIs. `[verified — rules §4]` |
| $40 coupon may not cover embeddings/rerank/caching; qwen3.7-max SG pricing unannounced at launch | Default to qwen-plus/flash for routine extraction; reserve qwen3.7-max for contradiction reasoning; stack the per-model free quota; keep everything on the Singapore endpoint. |
| Over-scoping the graph DB / eval harness | Freeze the MVP four-part loop on **SQLite** first; graph viz / sleep-time / eval = strictly post-MVP. |
| A sharp judge: "ADRs already do superseded; KB tools already detect contradictions" | **Pre-empt it on stage** — concede generic contradiction detection exists, then claim the defensible *combination* (AEC dependency graph + auto invalidation + rationale + a tamper-evident, attributable record). |
| Cost stats are mostly medium/low-confidence | Anchor impact on the **high-confidence** items (Building Control Act s.9 verbatim, reg 22(e) verbatim, Toh Guan Road 40 buildings, McKinsey $1.6T); present rework figures as "industry-reported." |

## 8. The seven strategic moves (the synthesis, distilled)

1. Make **"active premise-invalidation on an AEC decision-dependency graph"** the entire identity — it's the one thing no competitor ships and it photographs beautifully as the red alert.
2. Lead every judge-facing surface with the **Singapore QP-liability wedge (Building Control Act s.9 + the reg 22(e) gap)** — highest confidence, highest impact, maximises the 25% bucket.
3. **Bank the MCP/custom-skills hook concretely** — implement `capture_decision` + `check_invalidation` as Qwen-Agent MCP tools; build to both 30% descriptions.
4. Ship the **four-part loop on SQLite first**; resist the graph-DB/eval-harness temptation until the demo is filmable.
5. **Hard-code one deterministic storyline** with a tiny HRB/ADB rule-pack so the centrepiece never misfires.
6. **Stay honest** on novelty and statistics — a credible team scores higher than an overclaiming one.
7. **Before the deadline:** verify video length + deployment clause on the live page; confirm repo is public *with* an OSS license; keep inference on the Singapore endpoint; deploy to Alibaba as insurance.

---

*Next:* [04 · Qwen Tech Reference →](04-qwen-tech-reference.md) · [05 · Competitive Landscape →](05-competitive-landscape.md) · [06 · Open Questions →](06-open-questions.md)
