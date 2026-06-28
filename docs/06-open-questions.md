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
| A5 | **Demo storyline = "Maple Wharf" facade (terracotta → ACM) golden-thread thread.** | Highest blast-radius, photogenic red alert, maps 1:1 to the golden thread. The other 3 worked examples (parking, floor-to-floor, core) are backups. | Swap to parking/floor-to-floor/core if you prefer (all in [01](01-aec-direction.md) §4). |
| A6 | **Scope = one project, one deterministic storyline, done well.** No BIM/IFC integration, no multi-tenant, no firm-wide memory. | ~9 days to our 7 Jul target; a working four-part loop beats an unfinished elegant system. | Add stretch features only after C1–C6 pass (see [00](00-brief.md) §7). |
| A7 | **Deterministic AEC rule-pack gates the demo alert.** | So the centrepiece never misfires on stage; doubles as proof of domain depth. | Pure-LLM detection if you're confident — but I'd keep the rule gate for the recording. |
| A8 | **Build to BOTH 30% judging descriptions.** | Sources conflict on which 30% bucket owns "Qwen API/MCP use" vs "architecture/code quality." | N/A — this is the safe play; keep it. |

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

---

## C. Decisions only you can make (when you're back)

1. **Team & division of labour** — ✅ *2-person team.* The build plan in [03](03-hackathon-strategy.md) §6 targets a 7 Jul submission; when you're ready I'll split it into two parallel workstreams along the function-contract interface (memory core ↔ agent/demo).
2. **Region/jurisdiction focus** — ✅ *Resolved: you're in Singapore.* See **[07-singapore-angle.md](07-singapore-angle.md)** — Singapore has no golden thread, but the **QP personal-liability** regime is a stronger home-market wedge. Recommended framing: Singapore → China → UK (one line). **Still to decide together:** do you fully localize the demo to Singapore ("Tanglin Rise"), or keep UK + SG variants? And do you want me to execute the doc rewrites in 07 §6 now or after you align?
3. **Should I scaffold the code now?** I can stand up the repo: schema + SQLite store + the `capture_decision` / `check_invalidation` Qwen-Agent tools + the Maple Wharf transcripts + a thin CLI, so you have a running spine on day one. Say the word.
4. **Keep Idea B (Agent Society, Track 3) as a documented fallback?** I parked it; I can write a one-pager so it's not lost, but Track 1 is clearly the stronger fit and I recommend full focus there.
5. **Demo medium** — CLI with a TUI panel (fast to build, films fine) vs a thin web UI (prettier, more time). I'd start CLI, upgrade only if time allows.
6. **Real vs fictional transcripts** — I've written fictional ones (you control the storyline + can make the alert deterministic). If you have a *sanitised* real design-meeting transcript, it would add authenticity — but mind confidentiality/IP.

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
