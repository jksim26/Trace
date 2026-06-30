# Trace — Ambient Decision-Memory Design Spec

*Locked product direction · 2026-06-30 · for the Qwen Cloud hackathon (Track 1, MemoryAgent), internal submit 7 Jul.*
*This spec restates the locked direction and points to the canonical docs; it does not duplicate them. Confidence tags: `[verified]` / `[web search]` / `[inference]`.*

---

## 1. Locked product definition

**Trace is an ambient, proactive decision-memory agent for AEC — automation, not a tool.** It is *there* doing the job alongside the design conversation, not a panel you remember to open and query. **Active push, not passive pull** is the north star (doc 05 calls active push "the single sharpest differentiator").

It does four things no existing tool does together:
- **Captures** every design decision + rationale as it is made (meetings, RFIs, MOMs) as a structured record.
- **Knows** which decisions are currently **valid vs superseded** at any moment (bi-temporal validity).
- **Fires** an alert the instant a new decision **falsifies the premise** an earlier valid decision relied on — *active premise-invalidation*, the one thing no competitor ships.
- **Preserves** history immutably — superseded, never deleted — leaving a queryable "who changed what, when, why" chain.

Engine = a **bi-temporal decision-dependency graph on SQLite + a vector index** (not Neo4j for the hackathon; Neo4j + DashVector named as the production path). Full architecture in [02-architecture.md](../../02-architecture.md).

**Headline use case — handover.** When a senior leaves, the rationale walks out the door and a clean 1–2-month handover is rarely possible. Because Trace captures decisions *as they are made* — **consensual capture-as-you-go, not surveillance** — the handover record builds itself continuously instead of being reconstructed under pressure. `[inference]`

**Framing guardrails (do not drift):** proactive retrieval ends the needle-in-100-folders hunt, but it is **decision-aware surfacing, not "better search"** — Trace does not claim to out-search Glean/Copilot. Long-term memory is **bounded and growing toward firm-wide**, governed by write + forgetting logic so it stays *current*; the product reasons about **validity, not corpus size**. Do not lead with "ingest everything / answer anything" — that commodity space is owned by Glean, Microsoft 365 Copilot, and AEC's Workorb / Knowledge Architecture. `[inference]`

**Security moat (ROADMAP, not a demo claim).** The hackathon runs on **hosted Qwen Cloud** (required; Singapore DashScope endpoint), so for the demo data does leave to Alibaba Cloud. Because Trace is Qwen-native, the same design can run on **open-weight Qwen on-prem / air-gapped** — nothing leaves the firm's server — which SaaS incumbents structurally cannot match. Caveat: flagship `qwen3.7-max` is API-only, so an on-prem build would run a smaller open-weight Qwen. `[web search / general knowledge — not independently verified]`

**Jurisdiction.** Singapore-localized demo — **"Tanglin Rise"**: SCDF Fire Code 2023 Cl 3.5 (non-combustible over 15 m); Building Control Act s.9 QP personal criminal liability; Toh Guan Road fire precedent — with the UK golden thread as a one-line precedent (per docs 06/07).

---

## 2. Demo scope — the 7-July cut (build-vs-stage)

**BUILD FOR REAL — the four-part loop, end to end, on one deterministic storyline (C1–C4):**
**capture → invalidate (+ push alert) → recall-to-budget → audit.** This is the spine; C2 (the push alert) is built *second*, right after the store, so everything after it is polish, not core.

**STAGE — exactly one ambient "hero" moment:** the user opens the **2nd-storey drawing** and Trace proactively pops a context card — *"3 decisions here · 1 pending confirmation · facade spec superseded 3 weeks ago"* — with no prompt. Real enough to film, **without building a full screen-watching daemon.** The staged moment sells *automation, not a tool*; the real four-part loop proves it. `[team decision]`

**Explicitly OUT of scope for the hackathon:** live BIM/IFC integration; a multi-project / firm-wide knowledge base; multi-tenant SaaS with auth; a general-purpose contradiction detector; a full screen-watching ambient daemon. Post-MVP / stretch only (after the loop is filmable): blast-radius graph visualisation, sleep-time consolidation, a LongMemEval-style eval harness, the other worked examples, a real graph DB. (Brief §8; doc 03 §6.)

---

## 3. Success criteria (definition of done)

From [00-brief.md](../../00-brief.md) §7:
- **C1 — Capture:** ingest a transcript → correct structured decision record (rationale + assumptions + author + timestamp); reads back accurately.
- **C2 — Invalidate:** a later contradicting decision makes the agent **fire a conflict alert unprompted**, name the prior decision it breaks, and explain why — reliably on the storyline.
- **C3 — Recall under budget:** answer "why X, and can we still change it?" by pulling only currently-valid decisions into a **visible token budget**, and **abstain** ("no decision on record") when none exists — both on camera.
- **C4 — Immutable trail:** the superseded decision is preserved with a `superseded_by` link, not erased; the audit/history view walks the chain.
- **C5 — Qwen-native:** `capture_decision` and `check_invalidation` exposed as **MCP tools / custom skills** via Qwen-Agent; the agent calls them as tools.
- **C6 — Submittable:** public, **open-source-licensed** repo + architecture diagram + ≤ 3-min demo video + deck + written description on Devpost.

Plus the staged ambient beat:
- **C7 — Ambient surfacing (staged hero beat):** opening the 2nd-storey drawing makes Trace proactively pop the context card (above) with no prompt; staged real enough to film, no full screen-watching daemon. `[inference — staged for demo]`

---

## 4. Data model + five-part memory architecture

Defined in full in [02-architecture.md](../../02-architecture.md) (§3 data model, §4 five-part table) — **named here, not duplicated:**

- **Data model:** `Decision` node (statement · discipline · author · rationale · assumptions · brief_ref · importance · bi-temporal `valid_from/valid_to/recorded_at/superseded_at` · status) + edges `ASSUMES`, `DEPENDS_ON`, `SUPERSEDED_BY`, `AFFECTS`. Three stores: **episodic log** (raw transcript chunks), **semantic decision graph** (system of record), **vector index** (embeddings). Storage = **SQLite + vector index**.
- **Five-part memory architecture** (doc 02 §4): **short-term** (live conversation buffer + MemGPT-style core block); **long-term** (decision graph + episodic log + vector index); **write logic** (`capture_decision` = *compile, not retrieve* — compress a meeting into one structured record); **retrieval logic** (hybrid retrieve → composite re-score → **retrieve-to-budget**); **forgetting logic in two tiers** — (1) passive decay/dedup, (2) **active premise-invalidation**, the differentiating tier most stacks leave empty. A thin **ambient delivery layer** on top decides *when to surface unasked* (the C7 push).

---

## 5. Build order (from [02-architecture.md](../../02-architecture.md) §9)

1. Decision schema + SQLite store + never-delete supersession. *(spine)*
2. `capture_decision` via qwen3.7-max function-calling on one transcript. *(C1)*
3. `check_invalidation` = rule-pack + LLM premise check; push the alert. *(C2 — centrepiece, do not cut)*
4. Hybrid retrieve + composite re-score + retrieve-to-budget + abstention + context-budget meter. *(C3)*
5. Audit/history view walking `superseded_by`. *(C4)*
6. Wrap 1–5 as **Qwen-Agent MCP tools**. *(C5)*
7. Thin UI/CLI to film the scenes + architecture diagram + README + OSS license. *(C6)*

Stage the C7 ambient card once steps 1–5 are filmable.

---

*Source docs:* [00-brief.md](../../00-brief.md) · [02-architecture.md](../../02-architecture.md) · [03-hackathon-strategy.md](../../03-hackathon-strategy.md) · [05-competitive-landscape.md](../../05-competitive-landscape.md) · [07-singapore-angle.md](../../07-singapore-angle.md)
