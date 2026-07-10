# 09 · Manual Requirements — What Only the Human Team Can Do

*Everything on this page is **human/manual** work — it is **not** part of the AI code build. Source items: [03-hackathon-strategy.md](03-hackathon-strategy.md) §5–6 and [06-open-questions.md](06-open-questions.md) §B (verify items) + §C (human-only decisions). Confidence tags: `[verified]` · `[web search]` · `[inference]` · `[team decision]`. Items marked **VERIFY LIVE** must be confirmed on the live Devpost rules page (it renders empty to automated fetch) before the deadline.*

> **Why this doc exists:** Trace is "automation, not a tool," but the *build* still has a handful of things the agent cannot do for the team — register a billing identity, claim a coupon, read a live rules page, point a camera, and confirm the storyline. They are collected here so none of them silently gate the 7-July submission. Dates: internal submit target **7 Jul 2026**; hard deadline **9 Jul 2026, 14:00 PDT** `[verified — timezone-checked]`.

---

## A. BLOCKERS — these gate the entire code build

**Nothing in the LLM loop (capture · invalidate · recall) can run *or be tested* against a real model until A1–A4 are done.** Until then the build only runs against stubs/mocks. This is the single most time-critical human task — do it first. `[verified — per 06 §C7]`

- [ ] **A1 · Create the Alibaba Cloud / Model Studio (Qwen Cloud) account.** Only the human team can do this — it is tied to your **billing identity**, not the agent. `[verified — per 06 §C7]`
- [ ] **A2 · Claim the $40 build coupon + Model Studio new-user free quota** (~1M free tokens/model, Singapore region, ~90-day window). Stack the per-model free quota to stretch the budget. `[web search — per 03 §1]`
- [ ] **A3 · Generate `DASHSCOPE_API_KEY` and put it in `Trace/.env`** (repo-root `.env`, already protected by `.gitignore`). This is the key the existing smoke-test `Trace/test_connection.py` loads via `load_dotenv()`. `[verified — read in repo]`
- [ ] **A4 · Smoke-test the Singapore endpoint** — run `Trace/test_connection.py` (base URL `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`, model `qwen-plus`) and confirm it returns. Then confirm a `qwen3.7-max` call returns too. *Verify: "TRACE connection successful." prints; a real model reply comes back.* `[verified — script in repo]`

> **Note (not a blocker, but tied to A):** the hackathon **requires hosted Qwen Cloud** (Singapore **DashScope** endpoint), so for the 7-July demo, data **does leave** to Alibaba Cloud. The on-prem / open-weight-Qwen security moat is **roadmap only** — keep it off the demo (see §D5). `[web search — not independently verified]`

---

## B. VERIFY LIVE before the deadline — ✅ RESOLVED 2026-07-02

*A full human read of the live rules page was done on **2026-07-02**; the verbatim capture is **[docs/12-devpost-official-rules.md](12-devpost-official-rules.md)**. All items below are now settled from the primary source except B6.* `[verified — live read 2026-07-02]`

- [x] **B1 · Demo-video length — RESOLVED: < 3 minutes.** "should be less than three (3) minutes. Judges are not required to watch beyond three minutes." `[verified — rules §4]`
- [x] **B2 · Alibaba Cloud deployment — RESOLVED: MANDATORY.** "Include Proof of Alibaba Cloud Deployment: You must demonstrate that the backend is running on Alibaba Cloud. Proof must be a link to a code file in their code repo that demonstrates use of Alibaba Cloud services and APIs." Not insurance — a required submission field. `[verified — rules §4]`
- [x] **B3 · Video host — RESOLVED: YouTube / Vimeo / Youku**, publicly visible; link on the submission form. No third-party trademarks or copyrighted music. `[verified — rules §4]`
- [x] **B4 · Repo/license — RESOLVED:** public + open-source license file, and the license "should be detectable and visible at the top of the repository page (in the About section)" — check GitHub detects the MIT `LICENSE` and shows it in About. Repo must contain "all necessary source code, assets, and instructions required for the project to be functional." `[verified — rules §4]`
- [x] **B5 · 30%-bucket pairing — RESOLVED:** "Sophisticated use of Qwen Cloud APIs — e.g., custom skills, MCP integrations" belongs to **Innovation & AI Creativity (30%)**; architecture/code quality/tech-stack belongs to **Technical Depth & Engineering (30%)**. The build-to-both mitigation stands. `[verified — rules §6]`
- [ ] **B6 · Coupon / quota scope** — still not answered by the rules page (only the $40 voucher process is). Check on the Qwen Cloud benefits page when claiming credits. `[web search — unconfirmed]`
- [x] **B7 · Dates — RESOLVED:** deadline **9 Jul 2026 2:00 pm PT**; judging 10–31 Jul; winners ~7 Aug. `[verified — rules §1]`
- [x] **B8 · Full live read — DONE 2026-07-02**; verbatim capture in doc 12. `[verified]`

**NEW obligations surfaced by the live read** (see doc 12 "New obligations"):

- [ ] **B9 · Testing access** — the submission must include "a link to a website, functioning demo, or a test build," free to use until judging ends (31 Jul). Plan: the deployed Alibaba Cloud instance (B2) doubles as this link.
- [ ] **B10 · "Significantly updated" explanation** — the project predates nothing (built inside the window), but the Devpost write-up should still state the build happened entirely within the Submission Period, since the repo's first commits are late June.
- [ ] **B11 · Blog Post bonus prize (optional, 10 × $500 + $500)** — publish a public blog/social post on the build journey with Qwen Cloud and include the link in the submission. Low effort, separate prize pool.

---

## C. Human deliverables (build by hand; the agent can draft, the team owns)

*These are the [03](03-hackathon-strategy.md) §5 submission boxes that are human work, plus the §6 "5–6 Jul" record-and-package row.*

- [ ] **C1 · Record the demo video, ≤ 3 min** — the 3-scene storyline with the on-screen **red invalidation alert** + **context-budget meter**, plus the staged ambient "hero" moment (user opens the 2nd-storey drawing → Trace pops "3 decisions here · 1 pending confirmation · facade spec superseded 3 weeks ago"). Public on YouTube/Vimeo/Youku (per B3). `[team decision — demo scope per 03 §6]`
- [ ] **C2 · Presentation deck.** `[verified — §5 box]`
- [ ] **C3 · Written project description on Devpost.** `[verified — §5 box]`
- [ ] **C4 · Architecture diagram** — turn the §8 text diagram in [02-architecture.md](02-architecture.md) into a clean visual (human design pass, even if agent-drafted). `[verified — §5 box]`
- [ ] **C5 · Flip the repo to public at submit time** — keep it private during the build, make it public **with the OSS license present** at the moment of submission (per B4). `[team decision]`
- [ ] **C6 · (Optional) Provide a sanitised real design-meeting transcript** — would add authenticity over the fictional transcripts, **but mind confidentiality / IP**. Optional; the deterministic fictional storyline is the safe default. `[team decision — per 06 §C6]`

---

## D. Decisions to confirm (only the human team can settle these)

- [x] **D1 · Final demo storyline = "Tanglin Rise" (Singapore)** — locked 30 Jun; **completed 10 Jul: the legacy "Maple Wharf" UK framing is fully removed** (code, rules, drawing, docs — replaced by "Pearl Vista" under the BCA Periodic Façade Inspection pack; the pitch is Singapore-only, no UK close). `[team decision — per 06 §A5/§C2, anchors per 07]`
- [x] **D2 · Jurisdiction doc-rewrites** — executed 10 Jul across README / docs 00-06, 10 / demo script / diagram, Singapore-only framing. `[done — per 06 §C2]`
- [ ] **D3 · Division of labour (2-person team)** — confirm the split of [03](03-hackathon-strategy.md) §6 into two parallel workstreams along the function-contract interface (memory core ↔ agent/demo). `[open — per 06 §C1]`
- [ ] **D4 · Demo medium** — CLI + TUI panel (fast, films fine) vs thin web UI (prettier, costs time). Recommend starting CLI, upgrade only if time allows. `[open — per 06 §C5]`
- [ ] **D5 · On-prem / open-weight Qwen — roadmap only, keep OFF the 7-Jul demo.** Confirm this is a post-hackathon decision, not a demo claim. Caveat: flagship **qwen3.7-max is API-only**, so an on-prem build runs a smaller open-weight Qwen. `[web search / general knowledge — not independently verified]`
- [ ] **D6 · Keep Idea B (Agent Society, Track 3) as a documented fallback?** Track 1 is the stronger fit; decide whether to park a one-pager so it isn't lost. `[open — per 06 §C4]`

---

*Back to sources:* [03 · Hackathon Strategy](03-hackathon-strategy.md) §5–6 · [06 · Open Questions](06-open-questions.md) §B–C · [07 · Singapore Angle](07-singapore-angle.md)
