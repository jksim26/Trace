# 06 · Open Questions, Assumptions & Decisions I Made for You

You asked me to use my best judgment and not block on questions. So this is the ledger of **(A) calls I made on your behalf** — reverse any of them — **(B) facts to verify on the live Devpost page** before the deadline, and **(C) genuine decisions only you can make.**

---

## A. Calls I made for you (reverse freely)

| # | Decision | Why | How to reverse |
|---|---|---|---|
| A1 | **Name = "Trace"** (chosen by the team, 28 Jun; was provisionally "Keystone"). | Speaks to traceability / the audit trail / provenance — *a trace of every decision and why it was made*; aligns with the golden-thread theme; short + demo-memorable. | Settled. Repo + all docs renamed to Trace. |
| A2 | **Lead with the UK golden thread / BSA-2022 wedge.** | Highest-confidence + highest-impact claim; converts a memory demo into legally-mandated infrastructure; maximises the 25% Problem-Value criterion. | If your region/judges aren't UK-oriented, demote it to "professional-liability defence (globally)" and lead with the rework numbers + the Hackitt quote. |
| A3 | **SQLite + vector index, not Neo4j**, for the build. | Zero-ops, trivially open-sourced, fast enough for one project's decisions; Neo4j+DashVector cited as the production path. | If you want graph cred, swap in Neo4j/Graphiti — but only after the MVP loop is filmable. |
| A4 | **qwen3.7-max for reasoning, qwen-plus/flash for routine extraction.** | Cost control; reserve the flagship for the hard contradiction reasoning. | Use qwen3.7-max throughout if the free quota covers it. |
| A5 | **Demo storyline = "Maple Wharf" facade (terracotta → ACM) golden-thread thread.** | Highest blast-radius, photogenic red alert, maps 1:1 to the golden thread. **Jurisdiction now locked to Singapore — the storyline localizes to "Tanglin Rise" (decision C2 + [07](07-singapore-angle.md) §4); "Maple Wharf" is the original UK framing, with the demo files still mid-migration.** The other 3 worked examples (parking, floor-to-floor, core) are backups. | Swap to parking/floor-to-floor/core if you prefer (all in [01](01-aec-direction.md) §4). |
| A6 | **Scope = one project, one deterministic storyline, done well.** No BIM/IFC integration, no multi-tenant, no firm-wide memory. | ~9 days to our 7 Jul target; a working four-part loop beats an unfinished elegant system. | Add stretch features only after C1–C6 pass (see [00](00-brief.md) §7). |
| A7 | **Deterministic AEC rule-pack gates the demo alert.** | So the centrepiece never misfires on stage; doubles as proof of domain depth. | Pure-LLM detection if you're confident — but I'd keep the rule gate for the recording. |
| A8 | **Build to BOTH 30% judging descriptions.** | Sources conflict on which 30% bucket owns "Qwen API/MCP use" vs "architecture/code quality." | N/A — this is the safe play; keep it. |
| A9 | **Product direction = ambient, proactive decision-memory agent — "automation, not a tool"** (locked by team + lead, 30 Jun). It is *there* doing the job, not a tool you pick up and query: active **premise-invalidation push** + proactive in-context surfacing, not passive pull. | The north star. Active invalidation-push is *"the single sharpest differentiator"* ([05](05-competitive-landscape.md), [07](07-singapore-angle.md)); no competitor ships it `[inference — from positioning]`. Sharpens, doesn't replace, the decision-memory core. | Settled — reverse the *framing*, never the engine. |
| A10 | **Demo scope (7 Jul) = BUILD the four-part loop for real, STAGE one ambient "hero" moment.** Build: capture → invalidate (+alert) → recall-to-budget → audit. Stage: user opens the 2nd-storey drawing, Trace pops *"3 decisions here, 1 pending confirmation, facade spec superseded 3 weeks ago"* — filmable without a full screen-watching daemon. | Proves the differentiating loop end-to-end while making the "ambient/automation" promise visible on camera; avoids sinking 9 days into a brittle always-on watcher. | Build the always-on ambient daemon only as a post-submission stretch. |
| A11 | **Long-term memory is BOUNDED & governed, not "universal knowledge."** Trace ingests project context (decisions, standards, the meeting stream) into long-term memory; the footprint grows toward firm-wide over time but is kept *current* by write + forgetting logic. The product reasons about **validity**, not corpus size. | Reconciles the "ingest everything / answer anything" instinct without competing on corpus with Glean / Microsoft 365 Copilot / AEC's Workorb / Knowledge Architecture `[web search — commodity space, not benchmarked]`. | Grow the footprint over time — but never lead with corpus size. |

### Naming (A1 — settled)
**Trace** is the chosen name (28 Jun). It speaks to traceability / the audit trail / provenance — *a trace of every decision and why it was made* — and aligns directly with the golden-thread / decision-memory theme. Also considered: *Keystone* (the provisional placeholder), *Goldthread / Golden Thread Agent* (directly the wedge, but verify trademark sensibilities), *Cornerstone*, *Provenance*, *Lodestar / Datum / Plumbline*.

---

## B. Verify on the LIVE Devpost page before the deadline

*(The Devpost rules page renders empty to automated fetch, so these came from mirrors/snippets and are not from a direct read.)*

1. **Demo-video length** — sources conflict: "< 3 min" (Devpost snippet) vs "max 5 min" (qwencloud.com). **Edit to ≤ 3 min** to satisfy either; confirm before upload.
2. **Deployment requirement** — a web-search summary says projects must be "deployed on Alibaba Cloud infrastructure." Unconfirmed. **Confirm; deploy to an Alibaba Cloud instance as insurance regardless.**
3. **Which 30% bucket** owns "sophisticated Qwen API/MCP use" vs "architecture/code quality." (Mitigated by building to both, but good to know.)
4. **Tail-end dates** (judging window ~10–30 Jul, winners ~7 Aug) rest on a single source; the **9 Jul 14:00 PDT deadline** is multiply corroborated.
5. **Video host** — must be public on YouTube/Vimeo/**Youku**; put the link on the form.
6. **Repo must be public AND open-source-licensed** (license file present). Confirmed via snippet; double-check the exact license requirement.
7. **Coupon scope** — whether the $40 coupon + free quota cover embeddings/rerank/context-caching, and qwen3.7-max's Singapore availability/price (unannounced at launch).
8. **Do a live human read of the full rules page before submit.** B1–B7 all rest on mirrors/snippets, not a direct read (the page renders empty to automated fetch). Open it in a browser, re-confirm the deadline, demo-video length, deployment + open-source-license requirements, and the eligibility/registration steps, then lock the checklist. `[unverified — pending live read]`

---

## C. Decisions only you can make (when you're back)

1. **Team & division of labour** — ✅ *2-person team.* The build plan in [03](03-hackathon-strategy.md) §6 targets a 7 Jul submission; when you're ready I'll split it into two parallel workstreams along the function-contract interface (memory core ↔ agent/demo).
2. **Region/jurisdiction focus** — ✅ *Resolved: you're in Singapore.* See **[07-singapore-angle.md](07-singapore-angle.md)** — Singapore has no golden thread, but the **QP personal-liability** regime is a stronger home-market wedge. Recommended framing: Singapore → China → UK (one line). **✅ Now locked (30 Jun):** fully localize the demo to Singapore — **"Tanglin Rise"** (SCDF Fire Code 2023 Cl 3.5 non-combustible **> 15 m**; **Building Control Act s.9** QP personal criminal liability; **Toh Guan Road** fire precedent), keeping the **UK golden thread as a one-line close** `[verified — anchors per [07](07-singapore-angle.md)]`. *Remaining process question:* execute the doc rewrites in 07 §6 now, or after you align?
3. **Should I scaffold the code now?** I can stand up the repo: schema + SQLite store + the `capture_decision` / `check_invalidation` Qwen-Agent tools + the Maple Wharf transcripts + a thin CLI, so you have a running spine on day one. Say the word.
4. **Keep Idea B (Agent Society, Track 3) as a documented fallback?** I parked it; I can write a one-pager so it's not lost, but Track 1 is clearly the stronger fit and I recommend full focus there.
5. **Demo medium** — CLI with a TUI panel (fast to build, films fine) vs a thin web UI (prettier, more time). I'd start CLI, upgrade only if time allows.
6. **Real vs fictional transcripts** — I've written fictional ones (you control the storyline + can make the alert deterministic). If you have a *sanitised* real design-meeting transcript, it would add authenticity — but mind confidentiality/IP.
7. **Qwen Cloud account + $40 coupon + `DASHSCOPE_API_KEY`** — *manual, and it gates the entire LLM build.* Only you can register the account and claim the coupon (your billing identity). The hackathon **requires hosted Qwen Cloud** (Singapore **DashScope** endpoint), so for the demo data does leave to Alibaba Cloud `[web search — per hackathon setup, not independently verified]`. Action: create the account, claim the **$40 coupon + free quota** (scope per B7), set `DASHSCOPE_API_KEY` in the repo env; until then capture/invalidate/recall can only run against stubs.
8. **On-prem / open-weight Qwen — a future (post-hackathon) decision, not a demo claim.** The product *can* run on open-weight Qwen on-prem / air-gapped so nothing leaves the firm's server — a security moat SaaS incumbents (Glean, Copilot) structurally can't match. Caveat: the flagship **qwen3.7-max is API-only**, so an on-prem build would run a smaller open-weight Qwen. `[web search / general knowledge — not independently verified]` Decide if/when this goes on the roadmap; keep it OFF the 7 Jul demo (which uses hosted Qwen Cloud per C7).

---

## D. Genuine research gaps (honest about what I couldn't pin down)

- No hard statistic for the **actual adoption rate of formal decision logs** on real projects — the "decisions live in email" claim is qualitative.
- Not confirmed by hands-on trial that **no AEC tool (Revizto/ACC) or second-brain (Supermemory) ships a hidden decision-invalidation feature** — the "does NOT" claims are inference from positioning.
- Whether a **2025–26 stealth/funded AEC startup** is already building design-decision/rationale memory (BuiltWorlds' "40 AI-Driven AEC Solutions 2026" list wasn't reviewed item-by-item).
- Exact **Building Safety Regulator Gateway-2 evidence requirements** (which decision types must be evidenced) — the regime tightened through 2024–26; confirm against current BSR guidance if you lean hard on Gateway 2.
- Whether **buildingSMART BCF/IFC** has an emerging decision-rationale/provenance schema a competitor could ride.
- Mem0's ADD/UPDATE/DELETE/NOOP (paper) vs an "ADD-only" 2026 blog variant — unreconciled; doesn't affect our design (we use SUPERSEDE, not DELETE).

---

*This ledger is the one place I've recorded everything I assumed or couldn't verify. Nothing else in the docs hides an unstated assumption.*
