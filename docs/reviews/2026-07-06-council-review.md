# Trace — Council Review (Round 2)

*Conducted 2026-07-06 · a re-review against the [2026-07-02 verdict](2026-07-02-council-review.md) (overall 6.5/10). The same five AI reviewers with adversarial mandates independently re-read the full repository, each tasked with judging the **improvement** — which of the prior top-5 recommendations were executed, and whether the previously-falsified claims are now genuinely fixed in code or merely re-worded. They debated in structured rounds (openings → rebuttals → independent fact-checks of disputed claims → closings), and the presiding judge synthesized the verdict. 28 agents, 12 fact-checked disputes.*

## Score trajectory

| Council member | Lens | R1 final | R2 opening | R2 after rebuttals | R2 final | Δ vs R1 |
|---|---|---|---|---|---|---|
| Aria Chen | The Hackathon Judge | 7/10 | 7.5/10 | 7.5/10 | 7/10 | 0 |
| Marcus Webb | The Staff Engineer | 6/10 | 7/10 | 7/10 | 7/10 | +1 |
| Vera Okafor | The Skeptic | 5/10 | 6.5/10 | 6.5/10 | 6.5/10 | +1.5 |
| Sol Andersson | The Champion | 7/10 | 8/10 | 7.5/10 | 7.5/10 | +0.5 |
| Ingrid Halvorsen | The AEC Domain Expert | 6/10 | 8/10 | 7.5/10 | 7.5/10 | +1.5 |
| **Overall** | Presiding judge | **6.5/10** | | | **7.0/10** | **+0.5** |

---

# The Council's Verdict on Trace

## 1. Executive verdict

Trace is a genuinely well-engineered bi-temporal memory spine wrapped in a reasoning story that the code does not fully deliver, submitted to the one track it fits almost perfectly. The council's five independent reviews converged hard: the data layer (two-axis `get_valid_asof`, hash-chained audit log, 8 keyless MCP tools, an honest 111-passed/1-skipped offline suite) is real and above hackathon grade, while the two headline "reasoning" features — the decision court and the four-rule invalidation gate — are thinner than the README. Fact-checking settled every load-bearing structural dispute in the skeptics' favor: the court verdict is a hardcoded constant (TRUE), capture emits only one attribute so 3 of 4 SCDF rules cannot fire from a live transcript (TRUE), and the entire presentation surface — video, deck, Devpost writeup — does not exist as a file (TRUE). The winning move now is not more code; it is building the pitch and telling the reasoning story honestly before a judge probes "what decides the verdict?" **Final overall score: 7.0 / 10.**

## 2. Scorecard

| Dimension | Score /10 | Rationale |
|---|---|---|
| Concept & novelty | 8.0 | Active premise-invalidation + forgetting-as-a-first-class-event is the box the memory-agent field genuinely leaves empty; maps 1:1 to Track 1's four stages. |
| Engineering quality | 7.5 | Bi-temporal spine is correct on the hard backdated-supersession case, tamper-evident audit chain with real negative tests, honest 111/1 suite — but reasoning layer is a deterministic gate dressed as adjudication. |
| Pitch honesty | 5.5 | README verbs (ambient, reasons, tamper-evident, "four rules gate") outrun the code on the reachable path; internal docs are honest but front-matter is not. Fact-checks confirmed the overstatements. |
| Domain fit | 8.0 | Failure mode is the authentic Grenfell/Toh Guan mechanism, QP liability wedge is legally literate — but the rulepack over-constrains its own cited clauses (Cl 3.5.4) and the alert renders an undisclaimed liability conclusion. |
| Hackathon readiness | 5.0 | Mandatory Qwen + Alibaba gates cleared, offline demo un-failable — but with the hard deadline (9 Jul) closing, the entire scored Presentation surface is still unbuilt. |

## 3. Where the council agreed

- **The bi-temporal spine is real and correct.** All five accepted `get_valid_asof` (store.py:184-205) handles both the knowledge and validity axes, proven by test_timetravel.py:30-48; the SHA-256 hash chain detects both forgery and deletion. Marcus, Sol, and Vera independently verified it.
- **The offline suite is honest: 111 passed / 1 skipped.** Verified four times across members and the independent checker. (Aria's opening 105/2 was the lone miscount, retracted.)
- **The decision court does not adjudicate.** Unanimous by close — court.py:109-110 hardcodes `verdict="REJECT"` on any alert; the three Qwen roles supply prose only.
- **Capture reaches only 1 of 4 SCDF rules end-to-end.** capture.py:50-57 emits only `cladding_combustible`; PROJECT_CONTEXT hardcodes 95m/7.5m, killing the boundary and low-rise limbs.
- **The audit chain is tamper-evident, not tamper-proof.** No key, no external anchor; recomputable by anyone with file write access, and `verify_audit_chain` never cross-checks snapshots against the live decisions table.
- **The presentation surface does not exist.** No .mp4/.pptx/deck file, no video URL anywhere in the repo — only shot-lists. The single most consequential gap with the deadline closing.

## 4. The sharpest disagreements — and who won

**Clash 1 — Is the decision court a "money shot" or "theater"?**
Aria and Sol framed it as the differentiating money shot; Marcus, Vera, and Ingrid called it theater — a hardcoded constant. **Marcus/Vera/Ingrid won.** Fact-check: TRUE — `verdict="REJECT"` is a literal in the alerts branch, LLM outputs never touch the decision. Aria's fallback ("rule-gating a life-safety verdict is the *correct* design") has merit as engineering, but she conceded the "money shot" framing oversold the LLM's causal role. The court is defensible as design; it is indefensible as advertised adjudication.

**Clash 2 — "Four rules gate the alert": real capability or unit-test-only?**
Aria's opening implied breadth ("reasons about decisions over time"); Marcus and Vera argued 3 of 4 rules are dead end-to-end. **Marcus/Vera won decisively.** Fact-check: TRUE — only SCDF-Cl3.5-noncombustible fires from a live transcript; the other three require hand-built unit-test contexts. Sol conceded and dropped half a point; Aria conceded in her close. This is the single biggest pitch-vs-code gap.

**Clash 3 — Does the alert assert a *named individual's* criminal liability? (Ingrid vs Sol)**
Ingrid cited fire.yaml:27 + demo-script.md:43 to claim the code names "K. Lim." Sol challenged: the code says only generic "the QP"; the name lives solely in the storyboard. **Sol won — this is the one place a skeptic overreached.** Fact-check: FALSE — the named pairing exists only in demo-script.md; code carries only the anonymized form. Ingrid and Vera both withdrew the "in code" version cleanly. The remedy shrinks from re-architecture to deleting one narration line plus a disclaimer.

**Clash 4 — Is the SCDF rulepack a moat (cited clauses) or a liability (unfaithful encoding)? (Sol vs Ingrid)**
Sol banked "real clauses with official URLs" as moat-grade strength; Ingrid argued citation ≠ fidelity. **Ingrid won.** Fact-check: TRUE — fire.yaml:50-54 requires `class_0` only, dropping both the timber-9mm and Class-B limbs that the team's own source treats as compliant, so a real deployment false-positives on compliant facades. Citation is not encoding fidelity.

**Clash 5 — Named-QP liability: fatal adoption blocker or wrong scoreboard? (Ingrid vs Aria)**
Ingrid called the undisclaimed liability assertion the biggest blocker after capture; Aria argued no Track 1 judge deducts for adoption-friction and the concrete stakes *win* presentation points. **Split decision.** Aria is right on the scoreboard (this is a MemoryAgent judging rubric, not a procurement review), but Ingrid is right that the disclaimer gap is real and near-zero-cost to fix — so it costs nothing to close and should be closed before filming. Neither position was falsified; both survive.

## 5. Claims that did not survive fact-checking

- **"The decision court where three agents argue and a judge writes the verdict" (pitch framing)** — PARTIAL/overstated. Verdict is a hardcoded constant; the LLM roles are causally inert on the outcome (court.py:98-114, verdict TRUE).
- **"Four rules gate the alert" (README:37) as a live capability** — PARTIAL. Only 1 of 4 fires from a real transcript; the rest are unit-test-only (TRUE).
- **"105 passed / 2 skipped" (Aria's opening evidence)** — FALSE. The suite is 111/1 (TRUE). Retracted by Aria.
- **"The alert asserts a *named individual's* criminal liability... lives in code" (Ingrid/Vera)** — FALSE. Code names only a generic "the QP"; "K. Lim" appears only in demo-script.md narration. Withdrawn by both.
- **"Tamper-evident... the defence a criminally liable engineer has never had" (README:11)** — PARTIAL. Tamper-evident against accidents (tests prove it), not against a motivated party with DB write access; `verify_audit_chain` never cross-checks against the decisions table (TRUE).
- **"The golden thread the Building Safety Act makes legally mandatory" (README:11)** — overstated. A keyless SHA-256 chain in the same SQLite file, outside the ISO 19650 CDE, is a complement to the golden thread, not the thread itself (Ingrid, uncontested).

## 6. Top 5 recommendations

1. **Build the presentation surface — record the offline demo video, finalize the Devpost writeup and deck.** It is the entire remaining scored critical path and none of it exists. **Effort: 8-12h.** *Championed by Aria (and Sol).*
2. **Reframe the court honestly on camera and in the README as "rule-gated verdict with LLM-generated rationale."** Neutralizes the one lethal judge probe ("what decides the verdict?") at zero code cost. **Effort: 1-2h.** *Championed by Marcus (and Sol).*
3. **Extend capture.py's record_decision schema to emit `boundary_distance_m`, `cladding_class_0`, and `is_composite`.** Turns "four rules gate the alert" from unit-test-only into a true end-to-end capability — makes the pitch true rather than humbler. **Effort: 3-5h.** *Championed by Vera.*
4. **Strip the named individual from demo-script.md:43 and add one advisory disclaimer** ("flags premise conflicts for QP review; not a legal determination") to the alert output and README. Removes the line counsel would strike, at near-zero cost. **Effort: <1h.** *Championed by Ingrid.*
5. **Fix the Cl 3.5.4 over-constraint** — add the timber-9mm and EN 13501-1 Class B limbs to the rule so it stops false-positing on compliant facades, and consider anchoring/signing the audit chain to address the tamper-proof gap. **Effort: 2-4h (rule); 4-6h (anchoring, optional).** *Championed by Ingrid (rule) and Marcus/Vera (chain).*

## 7. The one-line summary a judge would write

*An exceptionally honest, correctly-built bi-temporal memory spine that ships the one feature the field skips — but the "reasoning court" is a rule-gated constant and the pitch video doesn't exist yet; finish the story truthfully and it's a finalist. **7.0/10.***


---

# Appendix: The Full Debate Record

## A. Opening Statements

### Aria Chen — The Hackathon Judge · 7.5/10

> **A top-quartile Track 1 contender with an un-failable offline demo and a category-defining hook, but the winning surface (video, deck, Devpost writeup) is still unbuilt, and that is the entire remaining risk.**

I judge one question: does this win Track 1? On concept and code, this is the strongest MemoryAgent positioning I have seen this cycle. The three-pillar table (README:21-26) maps one-to-one onto the official track wording: "efficient storage/retrieval" to a bi-temporal never-delete store; "timely forgetting" to active supersession plus the decision court; "recall within limited context" to retrieve-to-budget with a visible token meter. Most entries stretch to fit the rubric; Trace fits it like a glove, and does so while being categorically NOT the median "chatbot with a vector DB" entry. Active premise-invalidation plus bi-temporal time-travel plus a SHA-256 audit chain is a different animal, and "clash detection across time" (demo-script.md:14) is the kind of line a judge on entry 73 actually remembers.

The decisive thing for me is that the demo is un-failable. I ran `python cli.py --offline` (cli.py:176-182, replay.py) with no key and no network: it produced the red invalidation alert, then the three-Qwen-role court delivering a REJECT verdict with a defensible s.9 rationale, then recall-with-abstention and bi-temporal time-travel, instantly and deterministically. The court is a genuine money shot (pitch-kit 0:58-1:52), and offline replay removes the single most common hackathon death: a live call failing on camera. Most teams never build this. The mandatory pass/fail gates are also covered: real Qwen usage on the Singapore DashScope endpoint (court.py:26-27, capture.py) and a documented live Alibaba ECS deployment (deploy/INSTANCE.md, systemd service on 47.245.82.206) satisfy the backend-on-Alibaba clause that eliminates entrants at Stage One.

What keeps this at 7.5 and not 9 is that the surface judges actually score for Presentation does not exist yet. There is no video file, no deck, no YouTube link, no finalized Devpost prose anywhere in the repo, only shot-lists in docs/10-pitch-kit.md and demo/demo-script.md. With an internal target of tomorrow (7 Jul) and a hard 9 Jul deadline, recording a sub-3-minute video, building the six slides, and writing the description is now the entire critical path, and none of it is done. The code is finished; the pitch artifacts are not, and that is exactly backwards from where a winning entry sits 24-72 hours out.

Two softer risks compound it. First, the AEC/SCDF framing is niche: a generalist MemoryAgent judge must absorb Cl 3.5.1, s.9, reg 22 and PFI, and could read the fire-code rule-pack as vertical plumbing rather than memory innovation. Second, on camera the flagship "reasons about decisions over time" is a deterministic 4-rule YAML gate tuned to one storyline; the general LLM premise check only runs when the rule-pack is silent (invalidate.py header). Credit where due: the team demonstrably executed the prior council's fixes, so I nudge up half a point from the last verdict, but winning is a coin-flip that now turns entirely on production, not code.

**Strengths:**

- Track 1 alignment is literal and airtight, so a rubric-driven judge can score it without interpretive charity.
  - *Evidence:* README.md:21-26 three-pillar table quotes the official track language and pairs each pillar with a shipped module (store.py, invalidate.py/court.py, recall.py).
- The offline replay mode makes the demo un-failable, removing the single most common hackathon failure (a live API call dying on camera).
  - *Evidence:* cli.py:176-182 + replay.py; I ran `python cli.py --offline` with no key/network and it rendered the full four-scene story including the red alert and court REJECT verdict instantly.
- The decision court is a genuine money shot and a real differentiator versus the typical vector-DB memory entry.
  - *Evidence:* court.py:97-116 convenes Proposer/Guardian/Judge; the offline run produced a clause-cited REJECT rationale a liable QP could stand behind.
- The mandatory pass/fail gates (real Qwen usage + Alibaba deployment) are satisfied, clearing Stage One where many entries die.
  - *Evidence:* court.py:26-27 / capture.py use the dashscope-intl endpoint; deploy/INSTANCE.md documents a live ECS instance (47.245.82.206) with a systemd service and a test-gated deploy/deploy_alibaba.sh.
- The team executed the prior council's fixes, closing the pitch-vs-code gap and signaling it can finish.
  - *Evidence:* Offline replay, mcp_server.py, embeddings.py hybrid recall, and the get_valid_asof retroactive-supersession fix (store.py:184-205 now keys on superseded_at) all now exist; 105 passed / 2 skipped offline across 112 test functions.

**Weaknesses:**

- The judge-facing production artifacts that carry the Presentation score do not exist yet, making them the entire remaining critical path with less than 1-3 days left.
  - *Evidence:* No .mp4/.pptx/deck file and no YouTube/Vimeo/Youku link anywhere in the repo; only shot-lists in docs/10-pitch-kit.md and demo/demo-script.md.
- On camera the flagship 'active premise-invalidation' is a deterministic 4-rule YAML gate tuned to one storyline, not emergent memory reasoning; a judge who probes generalization finds it scripted.
  - *Evidence:* invalidate.py header: the LLM premise check 'runs only when the rule-pack is silent and a client is available'; rules/fire.yaml + PROJECT_CONTEXT (invalidate.py:36) are hardcoded to the Tanglin Rise building.
- The AEC/SCDF framing is niche and jargon-dense for a generalist MemoryAgent judge and risks reading as a vertical app rather than a memory-architecture advance.
  - *Evidence:* demo-script.md:11,42-44 leans on Cl 3.5.1 limbs, Building Control Act s.9, reg 22 and PFI, heavy cognitive load for a non-AEC judge in the mid-scenes.
- The pitch prose is maximalist and superlative-heavy, which a judge reading ~100 entries discounts; density is itself a legibility tax.
  - *Evidence:* README.md:11 is a single ~250-word sentence-dense block; 03-hackathon-strategy.md:42 claims 'the strongest impact story any Track-1 entrant is likely to have.'
- The deployed testing-access instance is a live-call surface: off-script judge questions depend on the key on the box, and without it the bubble degrades to bare deterministic abstention.
  - *Evidence:* deploy/README.md step 5 warns 'If /ask fails, check the key'; bubble.py serves live recall_decisions to Qwen, unlike the canned offline CLI.

**Claims staked (for cross-examination):**

- Running `python cli.py --offline` reproduces the full four-scene demo (capture, court REJECT verdict, recall+abstention, time-travel) with no API key and no network, eliminating the biggest demo-day failure mode; verified live.
- The README three-pillar table (README:21-26) aligns 1:1 with Track 1's official wording, and the entry ships active premise-invalidation + bi-temporal time-travel + audit chain, which the typical 'vector-DB chatbot' memory entry does not.
- The mandatory gates are covered: real Qwen calls on the dashscope-intl endpoint (court.py:26-27, capture.py) and a documented live Alibaba ECS deployment (deploy/INSTANCE.md, live URL 47.245.82.206, systemd service).
- No demo video, deck, or finalized Devpost writeup exists as a file in the repo (only scripts in docs/10-pitch-kit.md and demo/demo-script.md), and no YouTube/Vimeo link is present, so the entire Presentation surface is unbuilt with <3 days to the hard deadline.
- On camera the invalidation is a deterministic 4-rule YAML gate (rules/fire.yaml) tuned to one storyline; the general LLM premise check runs only when the rule-pack is silent (invalidate.py header), so the flagship 'reasons over time' claim is scripted in the filmed path.
- The team closed the prior council's falsified claims: offline replay, mcp_server.py, embeddings.py hybrid recall, and the get_valid_asof retroactive-supersession fix (store.py:184-205) all now exist, and 105 offline tests pass.

### Marcus Webb — The Staff Engineer · 7/10

> **The bi-temporal data spine is genuinely well-engineered and honestly tested, but the two headline "reasoning" features — the decision court and the rule-pack invalidation — are thinner than the pitch: the court's verdict is a hardcoded constant and the rule-pack is largely unreachable from the real capture path.**

I only trust code, and this code is better than most hackathon submissions — but not everywhere the README says it is.

What's real: a fresh-clone `pip install -r requirements.txt` then `python -m pytest` gives exactly 111 passed, 1 skipped, no key needed (the 1 skip is the live smoke test). The "111 offline tests" claim is honest. The bi-temporal store is the strongest asset. `get_valid_asof` (store.py:184-205) correctly handles BOTH axes — knowledge (recorded_at/superseded_at) and validity (valid_from/valid_to) — including the genuinely hard case: a backdated supersession recorded later must not rewrite what the record showed at an earlier date. test_timetravel.py:30-48 exercises exactly that and passes. Timestamp normalization to second precision (store.py:25-36) pre-empts the lexical mis-sort bug where "T00:00Z" sorts after "T00:00:00Z"; `_next_id` is MAX-based, not COUNT-based, to avoid id collisions (store.py:106-111). The SHA-256 hash chain is real tamper-evidence: test_audit.py forges a payload and deletes an event, and `verify_audit_chain` catches both at the right seq. Budget enforcement in recall is real, not cosmetic — `_pack` accumulates cost and breaks on overflow, carried across the valid-then-history packs (recall.py:77-90, 120-121). Tests mock the LLM with SimpleNamespace and assert on logic, which is the correct way to test LLM-adjacent code offline.

What's oversold: the "decision court where three agents argue and a judge writes the verdict" is theater. In court.py:99-116 the verdict is "REJECT" whenever the rule-pack fires and "ALLOW" otherwise — a hardcoded constant. The three role prompts produce prose that never feeds back into the decision; the Guardian could concede and the verdict would still be REJECT. The docstring is honest that the rule-pack gates the verdict, but the pitch language ("argues both sides, records the verdict") implies adjudication that does not exist. Worse, the invalidation gate is demo-hardwired: PROJECT_CONTEXT is a hardcoded 95m/7.5m building (invalidate.py:36,77) injected for every capture regardless of project, and capture only ever extracts cladding_combustible (capture.py:50-57). So of the four SCDF rules, only the height limb is reachable end-to-end, and only because the height is a constant. The "premise-aware" selection (invalidate.py:90-107) is lexical word-set intersection — string matching. The real reasoning path (llm_premise_check) needs a key and only runs as a silent fallback. Solid spine; the differentiators are thinner than advertised.

**Strengths:**

- Bi-temporal get_valid_asof is correct on the hard case — a backdated supersession recorded later does not rewrite earlier knowledge state
  - *Evidence:* store.py:184-205 (two-axis WHERE clause); test_timetravel.py:30-48 asserts D-001 shown on 15 Feb, D-002 after supersession is on record
- Tamper-evident audit chain is real and tested against actual tampering, not just happy-path growth
  - *Evidence:* store.py:76-103 (hash covers prev hash + canonical payload); test_audit.py forges payload (BROKEN at seq 1) and deletes an event, both caught
- Recall budget enforcement is genuine — a running cost accumulator that breaks on overflow, carried across the valid-then-history passes
  - *Evidence:* recall.py:77-90 (_pack breaks when used+cost>budget); recall.py:120-121 (used carried from valid pack into history pack)
- Defensive details that signal real experience: timestamp canonicalization, MAX-based id generation, refusal to fork a supersession chain
  - *Evidence:* store.py:25-36 (_normalize_ts), store.py:106-111 (_next_id), store.py:217-221 (raises on already-superseded)
- Tests exercise behavior with mocked LLMs — premise-aware selection, negative verdicts, LLM short-circuit — not just happy paths
  - *Evidence:* test_invalidate.py:64-87 (premise-aware not positional), :115-118 (negative verdict silent), :121-125 (rule hit short-circuits LLM via client=object())

**Weaknesses:**

- The decision court does not adjudicate: the verdict is a hardcoded constant (REJECT on any rule hit, ALLOW otherwise); the three agent outputs are prose with zero influence on the outcome
  - *Evidence:* court.py:99-116 — v.verdict = 'REJECT' unconditionally when alerts present; proposer/guardian/judge strings never feed the decision
- Invalidation is hardwired to the demo building's geometry, undermining the 'three projects, three code regimes' claim — every capture is evaluated as a 95m, 7.5m-to-boundary building
  - *Evidence:* invalidate.py:36 (PROJECT_CONTEXT hardcoded) injected unconditionally at invalidate.py:77
- The 'four-rule SCDF rule-pack' is largely unreachable end-to-end: capture extracts only cladding_combustible, so the boundary/class_0/composite/core rules have no path from a transcript — the live gate reduces to one boolean vs a hardcoded 95m
  - *Evidence:* capture.py:50-57 (only cladding_combustible in tool schema); rules/fire.yaml boundary rule needs <1m but geometry is 7.5m; class_0/is_composite/core_class0_or_b never populated by capture
- 'Premise-aware' invalidation selection is lexical word-set intersection (string matching), not reasoning; the genuine reasoning path needs an API key and only runs as a fallback
  - *Evidence:* invalidate.py:90-107 (_pick_breaks scores len(new_words & assumption_words)); llm_premise_check (invalidate.py:147) runs only when rules are silent and a client is supplied
- Bi-temporality is supersession-only: no transaction-time versioning of arbitrary field corrections (no update API), and a module-global SQLite connection is shared across threads with check_same_thread=False on an unenforced assumption
  - *Evidence:* store.py:39-45 (check_same_thread=False); mcp_tools.py:28-37 (shared global _conn); only add/supersede/verdict are audited — edits have no bi-temporal trace

**Claims staked (for cross-examination):**

- A fresh-clone `pip install -r requirements.txt` then `python -m pytest` yields exactly 111 passed, 1 skipped, with no DASHSCOPE_API_KEY set — the offline-test claim is honest.
- The decision court verdict is a hardcoded constant: court.py:99-116 returns 'REJECT' whenever check_invalidation returns any alert and 'ALLOW' otherwise; the three LLM role outputs never influence the verdict.
- Invalidation uses a hardcoded building geometry (95m height, 7.5m boundary) for every project — invalidate.py:36 and :77 — so the multi-project rule-gating story does not hold at the invalidation layer.
- The capture tool schema (capture.py:50-57) only ever emits cladding_combustible, so 3 of the 4 fire.yaml rules (boundary, class_0, composite-core) are unreachable from a real transcript; the live deterministic gate is effectively a single boolean against a constant height.
- get_valid_asof (store.py:184-205) is genuinely bi-temporal for supersession: it correctly excludes a supersession not yet known as of the query date, verified by test_timetravel.py:30-48, and the hash-chained audit log detects both payload forgery and event deletion (test_audit.py).
- 'Premise-aware' breaks-selection (invalidate.py:90-107) is lexical set-intersection string matching, not semantic reasoning; the real LLM premise check is a key-gated fallback that only runs when the rule-pack is silent.

### Vera Okafor — The Skeptic · 6.5/10

> **The engine is real and unusually honest in its internal ledger, but the README/pitch front-matter inflates a manual transcript-ingester plus a keyword matcher into an "ambient, reasoning, tamper-evident" agent — several headline verbs outrun the code.**

I went looking for lies and mostly found overstatement. Credit first, because I lose the room if I only swing: the "111 offline tests" claim is literally true — `pytest` gives 111 passed, 1 skipped (README.md:31). The never-delete store is real: `supersede_decision` does UPDATE+INSERT, and there is no DELETE anywhere in store.py:208-234. The SHA-256 hash chain genuinely exists and `verify_audit_chain` recomputes it (store.py:76-103). The MCP server exposes exactly 8 keyless deterministic tools, as advertised (mcp_server.py:215-218). And the research is rigorously self-audited — verification.md:16 catches its own 36-vs-40 building-count error and corrects to the primary SCDF source. This is not a vaporware repo.

Now the gaps. First, "ambient... captures every decision as the work happens (meetings, RFIs, minutes)" (README.md:11) is two different things wearing one coat. Capture is a single qwen-plus call over a pre-written transcript string (capture.py:102-118). The "ambient" half is a regex that matches a window TITLE to a project and pops a nudge card (ambient.py:40-48) — it captures nothing. The repo's own open-questions ledger admits this ("STAGE one ambient hero moment", A10), so internal honesty exceeds the front-page framing.

Second, "four rules... the gate" (README.md:37). Capture emits exactly ONE machine-checkable attribute, `cladding_combustible` (capture.py:50-57, 96-97). But `_ATTR_PATHS` wires five (invalidate.py:39-45), and boundary distance is hardcoded to 7.5 m. So three of the four SCDF rules can never fire from a real capture — they only fire in unit tests with hand-built contexts. One rule is reachable live.

Third, "premise-aware — names the specific stored assumption broken" (README.md:38). In the demo path that is bag-of-words set intersection, not reasoning (`_pick_breaks`, invalidate.py:90-107). The LLM premise check is real but runs only when rules are silent AND a key exists — never in the offline demo.

Fourth, "tamper-evident... the defence a criminally liable engineer has never had" (README.md:11). The chain, its algorithm, and its data all sit in one open-source SQLite file with no key or external anchor (store.py:76-103). Anyone who can edit the decisions table can recompute and rewrite audit_log undetectably — that IS the threat model for a liable party. It detects accidents, not adversaries.

No fabrication. But the top-of-funnel verbs — ambient, reasons, tamper-evident — are louder than the code underneath.

**Strengths:**

- Test count is exactly as claimed, not inflated — 111 passed, 1 auto-skipped live smoke test
  - *Evidence:* pytest run: 111 passed, 1 skipped; README.md:31
- Never-delete is genuinely enforced: supersession closes valid_to and links superseded_by with no DELETE in the codebase
  - *Evidence:* store.py:208-234
- The SHA-256 audit chain and verify_audit_chain are real and tested, not a slide claim
  - *Evidence:* store.py:76-103
- MCP server ships exactly the 8 keyless deterministic tools the README promises
  - *Evidence:* mcp_server.py:215-218
- Internal honesty is high: the offline banner and open-questions A10 openly disclose staging, canned replay, and deterministic alerts
  - *Evidence:* docs/06-open-questions.md:20
- Research confidence tags are earned — verification caught its own 36-vs-40 error and corrected to primary SCDF source
  - *Evidence:* .research/singapore/verification.md:16

**Weaknesses:**

- "Ambient capture as the work happens" is actually manual transcript ingestion plus a window-title matcher that captures nothing — two features fused rhetorically
  - *Evidence:* capture.py:102-118 and ambient.py:40-48
- "Four rules gate the alert" but capture emits only one machine-checkable attribute, so 3 of 4 rules are unreachable through the live pipeline and fire only in unit tests
  - *Evidence:* capture.py:50-57 vs invalidate.py:39-45
- "Premise-aware, names the specific broken assumption" is deterministic keyword-set overlap in the demo path, not inference
  - *Evidence:* invalidate.py:90-107
- "Tamper-evident defence" overstates: chain, algorithm and data share one keyless SQLite file, so a motivated editor can recompute and rewrite it undetectably
  - *Evidence:* store.py:76-103
- The advertised paraphrase/semantic recall requires DASHSCOPE_API_KEY and silently degrades to pure lexical in the keyless demo path
  - *Evidence:* recall.py:115-117, embeddings.py:29-40
- The filmed offline demo's "3 Qwen roles deliberate" court is replayed canned text from demo_replay.json, not live inference (disclosed, but it is the money shot)
  - *Evidence:* cli.py --offline banner; Trace/demo_replay.json

**Claims staked (for cross-examination):**

- Running pytest yields exactly 111 passed and 1 skipped, so the "111 offline tests" claim is accurate, not inflated.
- capture.py's record_decision tool extracts only one machine-checkable attribute (cladding_combustible), so 3 of the 4 SCDF rules in fire.yaml cannot fire from a real captured decision and are exercised only by hand-built unit-test contexts.
- In the offline/demo path, the 'premise broken' text is produced by keyword set-intersection in _pick_breaks (invalidate.py:90-107), not by any LLM reasoning; the LLM premise check runs only when rules are silent and a key is present.
- The audit chain is tamper-EVIDENT against accidental edits but not against a motivated party: the hashing algorithm and the audit_log live in the same open-source keyless SQLite DB, so an editor of the decisions table can recompute a consistent chain (store.py:76-103).
- The 'ambient' watcher/bubble matches window titles and displays a nudge card (ambient.py:40-48); it performs no decision capture, so 'captures every decision as the work happens' conflates manual transcript ingestion with a title matcher.
- The repo's own docs (open-questions A10, offline banner) disclose the staging, canned replay, and deterministic alerts that the README/pitch front-matter frames more confidently — internal honesty exceeds external framing.

### Sol Andersson — The Champion · 8/10

> **Trace is the rare hackathon entry that ships the one box every memory agent leaves empty — active premise-invalidation — on a genuinely bi-temporal, tamper-evident spine, tested and demo-hardened well past hackathon standard.**

Judge the loop the field skips. Track 1's brief names four stages — capture, store, retrieve, forget — and almost every memory demo builds the first three and hand-waves the fourth. Trace makes forgetting a first-class, reasoned event. When a new decision falsifies a stored premise, `check_invalidation` (invalidate.py:110) names the specific broken assumption, and `convene` (court.py:97) runs three Qwen roles to a persisted verdict. That is not a search box with extra steps; it is the unoccupied square the competitive doc identifies (docs/05:§3).

The spine underneath is real, not theatre. `get_valid_asof` (store.py:184-205) implements true bi-temporal semantics: a supersession recorded on 1 Mar but backdated to 1 Feb does NOT rewrite what the record showed on 15 Feb — and there is a test that asserts exactly that (test_timetravel.py:30-48). Most hackathon "time-travel" is a single `valid_to` column; this correctly separates the knowledge axis from the validity axis. Every write hash-chains SHA-256 over the prior event (store.py:76-103), and the tests actually tamper with and delete log rows and confirm detection (test_audit.py:48-63). I ran the suite: 111 passed, 1 skipped, offline, in 2.2s — the README's number is exact, not aspirational.

The engineering judgment is above grade. There is a deliberate certain/uncertain split: the LLM does language and argument, while an eight-tool MCP server (mcp_server.py) ships deterministic, keyless facts — rule-gate, as-of query, audit verification — so any client grounds on the parts that must not hallucinate. Degradation is designed, not accidental: hybrid recall falls straight back to the lexical path with no key (recall.py:60-74), and abstention stays deterministic. `cli.py --offline` replays canned responses so the on-stage demo cannot fail on a network blip — I ran it; the court's REJECT renders cleanly (demo_replay.json). The ambient trigger is one `match_title()` called by both the browser workspace and the Windows watcher (ambient.py:1-15), so "one brain, two worlds" is provable, not a slide.

The vertical choice is strategy, not decoration. Grounding "forgetting" in the UK Building Safety Act golden thread and Singapore QP criminal liability gives an abstract memory feature a concrete, high-stakes why-now that a generic notes demo cannot claim, and the SCDF rule-pack cites real clauses with official URLs (rules/fire.yaml).

I concede the honest limits and will not defend past them: the court's REJECT is rule-gated, so the LLM justifies a predetermined verdict rather than deciding it (court.py:98-114); the data is synthetic (scenarios.py); and the competitor "does NOT" claims are self-flagged `[inference]` (docs/05 preamble). But steelmanned, this is an 8: a coherent, tested, demo-proof system that does the one thing its track asks and its rivals skip.

**Strengths:**

- True bi-temporal recall that correctly resists retroactive rewriting — separates knowledge axis (recorded_at/superseded_at) from validity axis (valid_from/valid_to)
  - *Evidence:* store.py:184-205 get_valid_asof; test_timetravel.py:30-48 asserts a backdated supersession does not erase what the record showed mid-February
- Tamper-evident SHA-256 hash-chained audit log with negative tests that actually mutate/delete rows and confirm detection
  - *Evidence:* store.py:76-103 (_append_audit/verify_audit_chain); test_audit.py:48-63 tamper and delete cases both detected
- Active premise-invalidation is genuinely the empty box in the standard memory stack; here it names the specific broken assumption, not a generic 'conflict'
  - *Evidence:* invalidate.py:90-107 _pick_breaks names the broken premise; offline run prints 'premise broken: combustible external cladding is prohibited over 15 m'
- Test discipline far above hackathon norm — verified by running
  - *Evidence:* 112 test functions across 20 test files; `python -m pytest` yields 111 passed, 1 skipped in 2.2s offline, matching the README claim exactly
- Deliberate certain/uncertain architecture: a real MCP server (official SDK) exposes 8 deterministic, keyless, importable tools so clients ground on facts, not model output
  - *Evidence:* mcp_server.py:65-218 (list_projects/decisions_asof/check_compliance/verify_audit_chain/court_records); tool fns callable without the mcp package
- Designed graceful degradation and demo risk-management — the stage demo cannot fail on network
  - *Evidence:* recall.py:60-74 _sem_scores returns None on any embedding failure and falls back to lexical; cli.py --offline replays demo_replay.json (ran successfully)
- Strategic vertical: grounds abstract 'forgetting' in legally mandated golden thread + QP criminal liability, with real cited code clauses and official URLs
  - *Evidence:* rules/fire.yaml:16-71 four SCDF clauses with citation/provision/url; blast_radius names Building Control Act s.9 personal liability
- Intellectual-honesty discipline: [verified]/[web search]/[inference] confidence tags, a self-flagged unverified competitor table, and Alibaba deploy artifact for the mandatory rule
  - *Evidence:* README.md:108 confidence convention; docs/05 preamble flags 'does NOT' entries as inference; deploy/deploy_alibaba.sh present

**Weaknesses:**

- The 'decision court' does not actually decide — the verdict is hardcoded REJECT on any rule-pack hit; the three Qwen roles only supply justifying language for a predetermined outcome
  - *Evidence:* court.py:98-114 — convene sets verdict='REJECT' whenever check_invalidation returns alerts; the LLM roles feed rationale only
- All demonstrated memory is synthetic scaffolding — no real project data, users, or ingestion of live meetings; capture is shown on fictional transcripts
  - *Evidence:* scenarios.py:build_store fabricates the three project stores; demo/transcripts/ are authored fixtures
- The core novelty/moat rests on a competitor table the doc itself admits is unverified inference, not hands-on checks of Revizto/Supermemory/Mem0
  - *Evidence:* docs/05-competitive-landscape.md preamble: 'All does NOT entries are [inference]... not vendor disclaimers'
- The deterministic invalidation path is keyword-overlap, not semantic premise reasoning; the real LLM premise check only runs when the rule-pack is silent AND a key is present, so the headline 'reasons about decisions' is thin on the keyless path
  - *Evidence:* invalidate.py:90-107 _pick_breaks uses set-intersection word overlap; llm_premise_check (147-196) gated behind rule silence + client
- The rule-pack is four hand-curated fire clauses for one jurisdiction pair; the 'never mis-fire' reliability is scoped to a narrow demo surface, not general AEC coverage
  - *Evidence:* rules/fire.yaml holds 4 SCDF rules; rules/uk/ adds one reg 7(2) rule — coverage is demo-shaped

**Claims staked (for cross-examination):**

- Running `python -m pytest` in Trace/ offline passes 111 tests and skips 1 (the live smoke test), exactly matching the README's stated count.
- get_valid_asof (store.py:184-205) implements two-axis bi-temporal recall that correctly returns the pre-supersession decision for a mid-window date even when the supersession was backdated, proven by test_timetravel.py:30-48.
- The audit chain is real hash-chained tamper-evidence: test_audit.py:48-63 mutates and deletes log rows and verify_audit_chain detects both, returning the first bad sequence.
- Trace ships an actual MCP server on the official SDK exposing 8 deterministic tools that run with no API key and no network (mcp_server.py:65-218), and its tool functions are unit-testable without the mcp package.
- The invalidation alert names the specific broken stored assumption verbatim, not a generic conflict flag — verified in the offline CLI output ('premise broken: combustible external cladding is prohibited over 15 m').
- cli.py --offline runs the full four-scene demo including the court REJECT with zero API key or network, from demo_replay.json — a deliberate on-stage failure hedge.
- Conceded: court.py:98-114 hardcodes the REJECT verdict on any rule hit, so the court justifies rather than decides — the 'three agents argue it out' framing overstates the LLM's causal role in the outcome.

### Ingrid Halvorsen — The AEC Domain Expert · 8/10

> **The domain truth here is real — the failure mode, the rulepack, and the QP legal framing are the most code-literate AEC pitch I have reviewed — but the alert asserts a named individual's criminal liability with no disclaimer, and the capture bottleneck that decides whether this is a product is answered in one roadmap line.**

Thirty years in practice and compliance consulting have taught me to smell a screenplay. This is not one. The value-engineering transcript (demo/transcripts/02-value-engineering-2026-03-03.md) is the real failure: the fire engineer is explicitly absent (line 12), the contractor pitches a "visually identical" PE-core ACP under the "or equivalent" clause (lines 22-24), the design manager waves it through as "a finish-level change" (line 29), and the QP walks in late (line 31). That is precisely how Toh Guan Road and Grenfell happened — a cost decision silently falsifying a fire decision in a room that did not hold the rationale. I have sat in that meeting.

The rulepack is real-shaped, not toy. Trace/rules/fire.yaml faithfully encodes the SCDF clauses from .research/singapore/sg-sg-fire-cladding.md: the Cl 3.5.1 OR-limb (height >15 m OR boundary <1 m) is correctly split into two rules (lines 16-44), Cl 3.5.4 low-rise Class 0 (line 45), Cl 3.15.13 ACP core (line 59), each carrying an official SCDF URL. Classification usage is jurisdiction-correct: Class 0/BS 476 for Singapore, A2-s1,d0/A1 for the UK pack (rules/uk/fire.yaml:15). Maple Wharf's single-stair→two-stair supersession (scenarios.py:172-180) reflects the actual 2023 England second-staircase policy. The Singapore QP wedge (docs/07-singapore-angle.md) is legally literate and unusually honest — it frames the golden-thread absence as an *absence* (line 9), quotes Building Control Act s.9 verbatim, names the reg 22(e) structural-only gap, and lists what must NOT go on a slide (line 102). Mapping s.9's "ought reasonably to know" standard onto premise-falsification alerts (line 42) is genuinely clever.

But three domain landmines remain. First: the alert renders a legal conclusion about a named person. fire.yaml:27 and demo-script.md:43 assert accepting the substitution would "expose the named QP (K. Lim) to personal criminal liability under s.9." A software agent asserting an individual's criminal liability is itself a liability and defamation exposure; a firm's counsel strips that sentence before adoption. Second — and this is my unchanged finding from the 2 July council — no judge-facing document addresses the liability of the alert itself: a grep of README, brief, open-questions and pitch-kit for false-positive, alarm fatigue, or missed-alert reliance returns nothing; only .research/synthesis.md:45 buries it. For a product whose entire pitch is legal defensibility, that is the biggest adoption blocker after capture. Third: capture. Trace ingests clean fictional transcripts, yet the team's own docs/01-aec-direction.md:104 lists eight containers where decisions actually live; real meetings produce no transcript, "who types it in" is unanswered, and the watcher reads only window titles. That gap gets one roadmap line (docs/00-brief.md:76). The concept is domain-true; the unsolved parts are the honest hard parts of productization.

**Strengths:**

- The centrepiece failure mode is the authentic one: a fire-driven spec swapped for a cheaper visually-identical PE-core ACP under the 'or equivalent' clause, in a VE workshop the fire engineer is not in — this is the Toh Guan Road / Grenfell mechanism, dramatized faithfully, not a screenplay
  - *Evidence:* demo/transcripts/02-value-engineering-2026-03-03.md:12,22-24,29-31
- fire.yaml is a plausible SCDF rulepack that faithfully encodes its cited clauses — the Cl 3.5.1 height-OR-boundary limb is correctly split into two rules, low-rise Class 0 and ACP-core rules are present, and each rule carries the real SCDF provision text and official URL
  - *Evidence:* Trace/rules/fire.yaml:16-70 cross-checked against .research/singapore/sg-sg-fire-cladding.md
- The Singapore QP personal-liability angle is legally sound and honestly hedged: golden-thread absence framed as an absence not a rejection, s.9 and reg 22(e) quoted, and a slide-blocklist of unverified items (s.18, penalty ceilings, MCST case)
  - *Evidence:* docs/07-singapore-angle.md:9,13,24-35,102
- Jurisdiction-accurate fire classification and current regulation: Class 0/BS 476 for SG vs A2-s1,d0/A1 for UK, reg 7(2) combustible ban correctly stated, and the single-stair→two-stair supersession mirrors the real 2023 England second-staircase policy for residential over 18 m
  - *Evidence:* Trace/rules/uk/fire.yaml:12-20; Trace/scenarios.py:139-148,172-180
- The immutability critique I raised on 2 July is now substantively answered by a real SHA-256 hash-chained audit log over every write, with a working verifier — a genuine improvement over the plain SQLite file that existed then
  - *Evidence:* Trace/store.py:76-101; Trace/schema.sql:21-32; audit.py:11-17

**Weaknesses:**

- The alert asserts a named individual's criminal liability with no disclaimer — a defamation and product-liability exposure that a firm's counsel would strip before adoption; the tool states a legal conclusion it is not competent to render
  - *Evidence:* Trace/rules/fire.yaml:27,43 (blast_radius asserts 'the QP's personal criminal liability'); demo/demo-script.md:43 ('expose the named QP (K. Lim) to personal criminal liability')
- No judge-facing document addresses the liability of the alert itself — false-positive alarm fatigue, or a personally-liable QP relying on an invalidation the agent missed; for a defensibility product this is the largest unacknowledged adoption blocker after capture
  - *Evidence:* grep of README.md, docs/00-brief.md, docs/06-open-questions.md, docs/10-pitch-kit.md for false-positive/alarm-fatigue/advisory returns nothing; only .research/synthesis.md:45 mentions it
- The capture bottleneck — who types the decisions in — is essentially unanswered: Trace ingests clean fictional transcripts, but real decisions live in RFIs, change orders, VE logs, derogations, NCRs, transmittals and email (the team's own list), real meetings produce no transcript, and the watcher only reads window titles
  - *Evidence:* docs/01-aec-direction.md:104; Trace/watcher.py (title-bar only); scope cut to one roadmap line at docs/00-brief.md:76
- The 'immutable golden thread the law mandates' framing overclaims: the statutory golden thread must live in the ISO 19650 CDE and be handed to the Accountable Person; a self-contained hash-chained SQLite file outside the CDE (re-computable by anyone who can write it, with no external notarization/signing) is tamper-evident but is a complement to the golden thread, not the golden thread itself
  - *Evidence:* README.md:11 ('the golden thread the UK Building Safety Act now makes legally mandatory'); store.py:76-101 (chain stored in the same DB, no signing/anchoring)
- Rule fidelity is narrower than the clauses it cites: Cl 3.5.4 permits timber ≥9 mm OR Class 0 but the rule requires class_0 only, and Cl 3.15.13's NFPA 285 assembly and 1-hr-wall alternatives are named in the provision text but not encoded — so a real deployment would over-constrain and false-positive on compliant timber or NFPA-285 assemblies
  - *Evidence:* Trace/rules/fire.yaml:50-54,64-67 vs .research/singapore/sg-sg-fire-cladding.md ('timber 9mm+ or Class 0'; 'OR assembly to NFPA 285')

**Claims staked (for cross-examination):**

- The value-engineering transcript models the real AEC failure mode — a cost decision silently falsifying a fire decision in a room without the fire engineer or the rationale — and reads as a genuine meeting, not a screenplay (demo/transcripts/02-value-engineering-2026-03-03.md:12,22-31)
- Trace/rules/fire.yaml faithfully encodes its cited SCDF clauses: Cl 3.5.1's height-OR-boundary requirement is correctly split into two rules (lines 16-44) matching .research/singapore/sg-sg-fire-cladding.md, so the pack is real-shaped, not toy
- The Singapore QP personal-liability wedge is legally accurate and honestly bounded — golden-thread absence framed as absence, s.9 and reg 22(e) quoted, unverified claims explicitly blocklisted (docs/07-singapore-angle.md:9,102) — and is a sounder home-market hook than the UK golden thread
- The agent asserting a named QP's personal criminal liability (fire.yaml:27; demo-script.md:43) is itself a defamation/product-liability exposure with no disclaimer anywhere, and would be struck by any adopting firm's counsel
- No judge-facing document addresses the alert's own liability profile (false positives, alarm fatigue, or a QP relying on a missed invalidation) — a grep across README/brief/open-questions/pitch-kit returns nothing; it survives only in .research/synthesis.md:45
- The capture problem that separates a demo from a product is unsolved and under-acknowledged: Trace ingests clean transcripts while the team's own docs/01:104 lists eight other containers where decisions live, and integration gets a single roadmap line (docs/00-brief.md:76)

## B. Rebuttals

### Aria Chen (revised score: 7.5/10)

I judge one question — does this win Track 1 — and Round 2 sharpened rather than moved my answer. First, honesty: my opening cited "105 passed / 2 skipped." I re-ran it; the truth is 111 passed, 1 skipped in 2.27s offline (court.py suite included). Marcus, Vera, and Sol had the number right and I did not. Conceded.

Second, the decision court. Marcus, Vera, Sol, and Ingrid all land the same punch: court.py:110 sets verdict="REJECT" whenever check_invalidation returns alerts, with the ALLOW branch at :100 — the three Qwen roles supply prose, not the outcome. That is correct, and I concede the LLM does not adjudicate. But Marcus, I challenge your framing that this makes the court "theater" that loses points. Through a judging lens, a rule-gated verdict on a fire-code question is the RIGHT design, not a defect — you do not want an LLM freelancing a life-safety verdict on camera, and the Proposer/Guardian arguments at :106-108 are still live Qwen output. The risk is narrow and specific: it only costs points if a judge asks "what decides the verdict" on stage. The architecture doesn't lose; an unprepared answer to that one question would.

Ingrid — your named-QP-liability finding (fire.yaml:27, demo-script.md:43, both verified) is domain-true and I respect it, but I challenge its weight for THIS track. "A firm's counsel would strip that sentence before adoption" is a productization concern, not a scoring one. No MemoryAgent judge deducts for adoption-friction; and on camera that exact line — "expose the named QP (K. Lim) to personal criminal liability, Toh Guan Road, 1 fatality" — is the memorable punch that lands with a judge on entry 73. It wins points precisely because it is concrete and high-stakes. Real risk, wrong scoreboard.

Where the council genuinely moved me: the differentiator is thinner than the pitch on the reachable path. Vera and Marcus are right that capture.py:50-57 emits only cladding_combustible, so 3 of 4 fire.yaml rules never fire from a live transcript. I flagged the scripting in my opening, but the council deepened it. My thesis is unchanged: the code is finished, the winning surface — video, deck, Devpost prose — still does not exist (README:107 only cites the requirement). That, not the court internals, remains the entire remaining risk. I hold 7.5.

**Challenges raised:**

- **vs Marcus Webb** — on: *The decision court is 'theater' and 'oversold' — the hardcoded verdict makes the headline reasoning feature a liability.*
  - The verdict is rule-gated (court.py:110 REJECT on alerts, :100 ALLOW otherwise) — conceded — but a rule-gated verdict on a fire-code question is the correct design, not a defect: you do not want an LLM freelancing a life-safety verdict on camera, and the Proposer/Guardian arguments at court.py:106-108 are real Qwen output. From a judging lens this costs points only if a judge explicitly probes 'what decides the verdict'; the architecture itself is not a point-loser.
- **vs Ingrid Halvorsen** — on: *The alert asserting a named QP's criminal liability (fire.yaml:27, demo-script.md:43) is a defamation/product-liability exposure a firm's counsel would strip — the biggest adoption blocker after capture.*
  - Verified the text exists and the concern is domain-real, but it is a productization risk on the wrong scoreboard: no Track 1 MemoryAgent judge deducts for adoption-friction, and on camera the concrete named-QP + Toh Guan Road (1 fatality) line is exactly the high-stakes punch that lands with a tired judge — it earns Presentation points rather than losing them.
- **vs Vera Okafor** — on: *The filmed offline court is 'replayed canned text from demo_replay.json, not live inference' and this undercuts the money shot.*
  - demo_replay.json is confirmed a 6-item canned list and the offline court is replayed — but for a JUDGING lens this is a strength, not a weakness: cli.py --offline is what makes the demo un-failable on a network blip, the single most common hackathon death. The canned replay is a deliberate stage hedge, and every judge sees a working court regardless of connectivity.

**Concessions:**

- My opening test count was wrong: the offline suite yields 111 passed / 1 skipped (verified, 2.27s), not '105 passed / 2 skipped'. Marcus, Vera, and Sol had it right.
- The decision court does not adjudicate — court.py:110 hardcodes verdict='REJECT' on any invalidation alert and the three Qwen roles only supply rationale; I overstated it as a 'money shot' implying real argument-driven decision.
- Capture reaches only one of the four SCDF rules: capture.py:50-57 emits only cladding_combustible, so the boundary/class_0/composite rules in fire.yaml fire only in unit tests — the on-camera 'reasons about decisions over time' is thinner than the pitch, deeper than I credited in my opening.

### Marcus Webb (revised score: 7/10)

I ran it again, twice, with the key unset: 112 collected, 111 passed, 1 skipped, 2.1s. Sol, Vera and I all report exactly that. Aria reports "105 passed / 2 skipped across 112 test functions." That number is simply wrong, and it matters, because Aria's whole thesis is that the code is finished and de-risked — you cannot certify an un-failable demo on a test count you misread by six passes and a skip. Get the number right before you build the deck on top of it.

Aria, your second overstatement is the court. You wrote that `python cli.py --offline` "produced the court delivering a REJECT verdict with a defensible s.9 rationale." Look at what actually executes. Offline wires a ReplayClient (cli.py:176-178) into `convene`, and convene hardcodes `verdict="REJECT"` on any rule hit (court.py:109-113) — the three role strings are pure prose that never touch the outcome. The "defensible rationale" is a canned fixture string replayed from demo_replay.json, not reasoning a liable QP could stand behind. Vera called this correctly in her opening: it is replayed text, not live inference. Framing a predetermined constant plus a JSON fixture as an adjudicated verdict is exactly the pitch-vs-code gap you claim the team closed.

Vera and Ingrid — you are right about the audit chain and I concede it. My opening called it "real tamper-evidence," which is true against the accidental-edit threat the tests exercise (test_audit.py forges and deletes rows, both caught). But there is no HMAC key, no external anchor, and — I checked — `verify_audit_chain` (store.py:90-103) only recomputes the log's internal hash consistency; it never cross-checks the audit snapshots against the live `decisions` table. So a party with write access to the SQLite file can rewrite audit_log and recompute a consistent chain undetectably, and a straight edit of the decisions table is not even inspected by the verifier. For a product whose pitch is legal defensibility against a motivated, personally-liable party, that is the wrong threat model, and it trims my confidence in the flagship "golden thread" claim.

Sol, we agree on the spine and agree the court "justifies rather than decides." That convergence — three of five now say the two headline reasoning features are thinner than the README — is the real finding of this round. I hold at 7: excellent data layer, oversold reasoning layer.

**Challenges raised:**

- **vs Aria Chen** — on: *105 passed / 2 skipped offline across 112 test functions.*
  - Two fresh-clone runs with DASHSCOPE_API_KEY unset both give 111 passed, 1 skipped, 112 collected (verified via `python -m pytest -q` and `--collect-only`). Sol and Vera also report 111/1. Aria's 105/2 is a misread; the one skip is the live smoke test.
- **vs Aria Chen** — on: *The offline run produced the three-Qwen-role court delivering a REJECT verdict with a defensible s.9 rationale a liable QP could stand behind.*
  - In offline mode a ReplayClient is injected into convene (cli.py:176-178). convene hardcodes verdict='REJECT' on any rule hit (court.py:109-113); the proposer/guardian/judge strings never influence the outcome, and the 'rationale' is canned fixture text from demo_replay.json, not live reasoning. It is a predetermined constant plus a replayed string, not an adjudicated defensible record.
- **vs Vera Okafor** — on: *Anyone who can edit the decisions table can recompute and rewrite audit_log undetectably.*
  - Correct on the core point (no key/anchor, chain is recomputable) and I concede it. One refinement for the record: verify_audit_chain (store.py:90-103) only checks the log's internal hash consistency and never compares the audit 'add' snapshots (store.py:156-162) against the live decisions table — so a decisions-table edit alone is not even examined by the verifier, which is arguably weaker than Vera states.

**Concessions:**

- Vera and Ingrid are right that the audit chain is tamper-EVIDENT (against accidents, which the tests prove) but not tamper-PROOF against a motivated party: there is no secret key, HMAC, or external anchor, so anyone with write access to the SQLite file can recompute a consistent chain (store.py:76-103). My opening's 'real tamper-evidence' framing needed that qualifier.
- Sol's characterization that the court 'justifies rather than decides' is the accurate one; combined with Vera's and my findings, the majority now agrees the two headline reasoning features (court verdict, rule-pack invalidation) are thinner than the README.

### Vera Okafor (revised score: 6.5/10)

I re-ran the repo before swinging, and the strongest finding is a number. Aria, your opening rests on "105 passed / 2 skipped offline across 112 test functions" as proof the team executed the prior council's fixes. That count is wrong. `python -m pytest` in Trace/ returns 111 passed, 1 skipped, in 2.25s — verified live, twice. Marcus, Sol and I all independently got 111/1. A skeptic panel that cites the test count as evidence of discipline cannot itself miscount by six; it hands a judge the exact "did they actually run it?" opening we are supposed to close. Fix the number — the underlying point (offline suite is honest) survives, and I concede that much freely.

Sol, at an 8 you list "names the specific broken assumption, not a generic conflict" as a headline STRENGTH, then list the same mechanism as a weakness two paragraphs down. On the filmed keyless path that "naming" is `_pick_breaks` scoring `len(new_words & _words(assumption))` — bag-of-words set intersection (invalidate.py:90-107, confirmed). You cannot bank it as reasoning in the strengths column and disclaim it as keyword overlap in the weakness column; pick one. It is string matching, and the LLM premise check (invalidate.py:110-114 header) only runs when rules are silent AND a client exists — never in the demo you praise.

Aria and Sol both make the "decision court" a money shot. I now agree with Marcus and concede: court.py:97-116 sets verdict="REJECT" unconditionally whenever check_invalidation returns any alert (line 110), ALLOW otherwise; proposer/guardian/judge strings only decorate a predetermined outcome. A "court" whose verdict is a constant is theater, and it is the on-camera centerpiece — that is a scoring risk, not a strength.

Marcus, your PROJECT_CONTEXT point (invalidate.py:36,77 — every capture evaluated as a hardcoded 95m/7.5m building) is correct and sharper than my own "one reachable rule" framing; I adopt it. capture.py:50-57 emits only cladding_combustible, yet _ATTR_PATHS wires five attributes (invalidate.py:39-45), so three of four SCDF rules are dead end-to-end. Confirmed.

Ingrid, your defamation flag is real: fire.yaml:28,43 assert "the QP's personal criminal liability," and demo-script.md:27,43 escalate to the named individual "K. Lim." Note the nuance — the code names a generic QP; only the demo narration names the person — but a tool rendering an individual's criminal-liability conclusion is a genuine adoption blocker I under-weighted. Conceded. My thesis holds: honest engine, overstated top-of-funnel verbs.

**Challenges raised:**

- **vs Aria Chen** — on: *105 passed / 2 skipped offline across 112 test functions, cited as evidence the team executed fixes*
  - Factually wrong. python -m pytest in Trace/ returns 111 passed, 1 skipped in 2.25s (verified live). Marcus, Sol and I all got 111/1. Miscounting the test suite by six undermines the very discipline the number is invoked to prove.
- **vs Sol Andersson** — on: *Active premise-invalidation 'names the specific broken assumption, not a generic conflict' is a headline strength (score 8)*
  - On the keyless demo path the 'naming' is _pick_breaks scoring len(new_words & _words(assumption)) — bag-of-words set intersection (invalidate.py:90-107). Sol lists this same mechanism as a weakness. It cannot be banked as reasoning and disclaimed as keyword overlap simultaneously; the LLM premise check only runs when rules are silent AND a key exists (invalidate.py:110-114), never in the filmed demo.
- **vs Aria Chen** — on: *The decision court is a genuine money shot and real differentiator (court.py:97-116 convenes Proposer/Guardian/Judge)*
  - court.py:110 hardcodes verdict='REJECT' whenever check_invalidation returns any alert, ALLOW otherwise; the three role strings never feed the decision. A court whose verdict is a constant is theater, and it is the on-camera centerpiece — a scoring risk, not a differentiator.

**Concessions:**

- Marcus is right that PROJECT_CONTEXT (invalidate.py:36,77) injects a hardcoded 95m/7.5m building geometry into every capture, so the multi-project rule-gating story collapses at the invalidation layer — sharper than my own framing, adopted.
- Ingrid's defamation/product-liability flag is real and I under-weighted it: fire.yaml:28,43 assert 'the QP's personal criminal liability' and demo-script.md:27,43 name the individual 'K. Lim' with no disclaimer.
- Marcus and Sol correctly establish the court does not adjudicate (court.py:110 hardcoded REJECT); I now treat this as a confirmed on-camera risk, not just an overstatement.
- The offline test claim is honest at 111/1 — I concede the suite itself is not inflated, only Aria's recount of it is off.

### Sol Andersson (revised score: 7.5/10)

I steelman, but I don't fabricate, so let me start by cleaning up our own evidence. Aria, your headline strength cites "105 passed / 2 skipped offline across 112 test functions." That number is wrong. I ran `python -m pytest -q` at HEAD (last commit Sat 4 Jul) with no key: 111 passed, 1 skipped in 2.30s — matching Marcus, Vera and my own opening exactly. The correction cuts in the project's favour, so it costs the defence nothing, but a champion who quotes a phantom count hands the skeptics a free "he didn't run it" — so I retract 105/2 and we should all cite 111/1.

Marcus and Vera, you win the reachability argument cleanly and I concede it. I confirmed capture.py:50-57 emits exactly one machine-checkable attribute (cladding_combustible), and PROJECT_CONTEXT hardcodes height 95 / boundary 7.5 (invalidate.py:36). Cross-referencing fire.yaml: the boundary rule needs boundary<1 (dead at 7.5), the low-rise rule needs height<=15 (dead at 95), the ACP-core rule needs is_composite which capture never sets. So one of four rules is live end-to-end, and it's a single boolean against a constant. My opening's "reasons about decisions over time" over-implied breadth on the filmed path; I revise down half a point to 7.5 for that.

But Ingrid, I challenge your framing that "the alert asserts a named individual's criminal liability." The shipped alert does not. fire.yaml:28 blast_radius reads generically — "the QP's personal criminal liability (Building Control Act s.9)" — a role, not a person. The name "K. Lim" appears only in demo-script.md:43, the storyboard prose, not in any code path that check_invalidation or the court emits. That distinction matters for your remedy: counsel strikes one line of a demo script, not a re-architecture. The disclaimer gap in the storyboard is real and I concede it; the claim that the agent itself renders a named legal conclusion is not what the code does.

What survives every cross-examination is the spine, and nobody contradicted it: get_valid_asof's two-axis correctness under a backdated supersession (store.py:184-205, test_timetravel.py:30-48), the hash-chained audit log with real tamper/delete negative tests, and eight keyless MCP tools. That's the honest 7.5.

**Challenges raised:**

- **vs Aria Chen** — on: *105 passed / 2 skipped offline across 112 test functions.*
  - Wrong count. `python -m pytest -q` at HEAD with no DASHSCOPE_API_KEY yields 111 passed, 1 skipped in 2.30s — matching Marcus, Vera and my own runs. The real number is more favourable, but the stated 105/2 is not reproducible and undercuts the 'I ran it' credibility the strength depends on.
- **vs Ingrid Halvorsen** — on: *The alert asserts a named individual's criminal liability with no disclaimer (cites fire.yaml:27 and demo-script.md:43).*
  - The shipped rule/alert does NOT name a person: fire.yaml:28 blast_radius says generically 'the QP's personal criminal liability (Building Control Act s.9)' — a role. The name 'K. Lim' exists only in the storyboard prose demo-script.md:43, not in any code path check_invalidation or court.convene emits. So the fire.yaml citation does not support 'named individual'; the remedy is deleting one script line, not fixing the agent's output.
- **vs Marcus Webb** — on: *capture extracts only cladding_combustible so 3 of 4 fire.yaml rules are unreachable end-to-end.*
  - I re-checked and you are right — I concede this. capture.py:50-57 emits only cladding_combustible; invalidate.py:36 hardcodes height 95 / boundary 7.5, so fire.yaml's boundary (lt 1), low-rise (height lte 15) and ACP-core (is_composite) rules can never fire from a real capture. Only the height rule is live. This narrows my opening's breadth claim and I lower my score accordingly.

**Concessions:**

- Marcus and Vera are correct: capture.py:50-57 emits only cladding_combustible and invalidate.py:36 hardcodes the building geometry, so 3 of the 4 fire.yaml rules are unreachable from a live capture and the filmed deterministic gate is effectively one boolean against a constant height.
- The decision court verdict is a hardcoded REJECT on any rule hit (court.py:110); the three Qwen roles supply rationale only. I flagged this in my opening and Marcus/Vera confirm it — the 'three agents argue it out' framing overstates the LLM's causal role.
- Vera is right that the audit chain is unanchored and locally recomputable: hash algorithm and audit_log live in the same keyless SQLite file (store.py:76-103), so a party with write access to decisions can rebuild a consistent chain. It is tamper-EVIDENT to an outside verifier, not tamper-proof against the DB holder; adversarial use needs external anchoring/signing.
- Ingrid's disclaimer point stands for the storyboard: demo-script.md:43 asserts a named QP's criminal liability with no advisory disclaimer, and that is a legitimate presentation/liability risk to fix before filming.

### Ingrid Halvorsen (revised score: 7.5/10)

I came to defend domain truth, and the council has largely sharpened it rather than overturned it. Marcus, Sol and Vera independently establish that the "decision court" hardcodes REJECT (court.py:110) and that capture emits a single machine-checkable attribute, cladding_combustible (capture.py:50-57), leaving three of four SCDF rules unreachable from a real transcript. I confirmed both against the source and I concede them — they do not wound my thesis, they underwrite it. My central worry was always that Trace is a domain-true concept with a demo-shaped implementation, and this is exactly the shape of that gap.

But two colleagues overclaim in my territory. Sol, you list "the SCDF rule-pack cites real clauses with official URLs" as a moat-grade strength and score an 8 partly on it. Citation is not fidelity. Cl 3.5.4 in the team's own primary source permits "timber 9mm+ OR Class 0" (.research/singapore/sg-sg-fire-cladding.md:12), yet fire.yaml:53-54 requires class_0 eq true only — it silently drops the timber limb. Cl 3.15.13's "OR assembly to NFPA 285 / 1-hr fire-rated wall" alternative (research:13) survives only as prose in the provision string; the require logic (fire.yaml:64-67) never encodes it. A compliance officer deploying this over-constrains and false-positives on compliant timber and NFPA-285 assemblies. Real clauses, unfaithfully encoded — that is a liability, not a moat.

Aria, your risk inventory names "niche/jargon-dense framing" as the domain hazard. That is the lesser one. The alert asserts a named individual's criminal liability with no disclaimer — demo-script.md:43 and fire.yaml:28,43 both put "K. Lim / the QP's personal criminal liability" on screen. A grep for false-positive, alarm-fatigue or advisory across README, docs/ and demo/ returns nothing but the prior review doc. A tool that renders a legal conclusion about a specific person, and never once addresses its own liability profile, is struck by any adopting firm's counsel before jargon is ever discussed. That is the adoption blocker, and it is absent from your list.

I also hold my golden-thread caution: README.md:11 calls this "the golden thread the UK Building Safety Act now makes legally mandatory," but the statutory thread lives in the ISO 19650 CDE, and a keyless SHA-256 chain in the same SQLite file (store.py:76-101) is a complement, not the thread. Vera reaches the same place from the security side; I concede her framing.

**Challenges raised:**

- **vs Sol Andersson** — on: *The SCDF rule-pack cites real clauses with official URLs (rules/fire.yaml) — a strength grounding the vertical as strategy, contributing to an 8.*
  - Citation is not faithful encoding. The team's own source permits Cl 3.5.4 compliance via 'timber 9mm+ OR Class 0' (.research/singapore/sg-sg-fire-cladding.md:12) but fire.yaml:53-54 requires class_0 eq true only, dropping the timber limb; Cl 3.15.13's 'OR assembly to NFPA 285 / 1-hr fire-rated wall' path (research:13) appears in the provision prose but is absent from the require logic (fire.yaml:64-67). As a compliance instrument this over-constrains and would false-positive on compliant timber and NFPA-285 assemblies — the URLs are real, the encoding is not.
- **vs Aria Chen** — on: *The domain-facing risks are that the AEC/SCDF framing is niche and jargon-dense and that generalization is scripted; these are the softer risks around a strong entry.*
  - The risk inventory omits the larger domain hazard: the alert asserts a named individual's criminal liability with no disclaimer (demo/demo-script.md:43; fire.yaml:28,43 both name 'the QP's personal criminal liability under Building Control Act s.9'), and a grep for false-positive/alarm-fatigue/advisory across README.md, docs/ and demo/ returns nothing but the prior review doc. A tool rendering a legal conclusion about a specific person, silent on its own liability, is a defamation and product-liability exposure a firm's counsel strips before adoption — a bigger blocker than jargon.
- **vs Marcus Webb** — on: *The live deterministic gate is effectively a single boolean against a constant height.*
  - Correct but understated from the domain seat: the 95m height is not merely constant, it has no capture path at all — capture.py's schema (capture.py:50-57) has no height, boundary, class_0, is_composite or core field, and PROJECT_CONTEXT is injected unconditionally (invalidate.py:36,77). So the geometry that makes the one reachable rule fire can never originate from a meeting transcript; the demo's 'detection' is pre-loaded by a hardcoded building, which is a stronger indictment of the multi-project story than 'a single boolean' conveys.

**Concessions:**

- Marcus, Sol and Vera are right that the decision court does not adjudicate: court.py:110 sets verdict='REJECT' on any rule hit and the three Qwen roles only supply post-hoc justification — the 'three agents argue it out' framing overstates the LLM's causal role.
- Marcus and Vera are right that capture emits only cladding_combustible (capture.py:50-57), so three of the four fire.yaml rules are unreachable from a real transcript and fire only in hand-built unit tests — this sharpens, not softens, my capture-bottleneck finding: even the fire rulepack's advertised breadth is demo-shaped.
- Vera is right that the audit chain is tamper-evident against accidents, not adversaries: the algorithm and the audit_log share one keyless SQLite file (store.py:76-101), which is precisely why it is a complement to the golden thread, not the golden thread itself.
- Aria is right, and I verified it, that no demo video, deck, .mp4/.pptx or YouTube/Vimeo/Youku link exists as a file in the repo — the entire presentation surface is still unbuilt.

## C. Independent Fact-Check Verdicts

*Every factual claim the council disputed was routed to an independent verifier who ruled it against the actual code.*

**1. [TRUE]** The decision court verdict is hardcoded: convene() returns 'REJECT' whenever check_invalidation yields any alert and 'ALLOW' otherwise, and the three LLM role outputs never influence the verdict.

- *Evidence:* Trace/court.py:98-102 — convene() computes alerts = check_invalidation(...) (commented "deterministic evidence"); if not alerts, it returns Verdict(False, "ALLOW", ...) at line 100. Trace/court.py:103-114 — otherwise it takes alert = alerts[0] and constructs Verdict(conflict=True, verdict="REJECT", ...) at lines 109-110 with the literal string "REJECT" set unconditionally in the alerts branch. Trace/court.py:106-108 — proposer, guardian, rationale are LLM _role() calls; at lines 112-113 they are assigned only to for_argument=proposer, against_argument=guardian, rationale=rationale. The verdict field ("REJECT"/"ALLOW") is a literal in both branches and is never derived from proposer/guardian/rationale content.
- *Nuance:* The LLM outputs are not entirely inert — they populate the human-readable Verdict.for_argument/against_argument/rationale fields and are persisted to court_records (lines 82-88) and rendered (lines 122-127). But they have zero causal effect on the ALLOW/REJECT decision itself, which is fully determined by whether check_invalidation returns any alert. So the verdict value is hardcoded exactly as claimed.

**2. [TRUE]** The capture tool schema extracts only one machine-checkable attribute (cladding_combustible), so 3 of the 4 SCDF rules in fire.yaml are unreachable from a live captured transcript and fire only in hand-built unit tests.

- *Evidence:* capture.py:37-58 — the record_decision tool schema's `properties` has exactly ONE machine-checkable/attribute field: `cladding_combustible` (lines 50-57). All other properties (statement, discipline, rationale, assumptions, author, brief_ref) are free-text/metadata, not rule attributes. parse_tool_calls confirms the only attribute ever populated: capture.py:95-98 sets `attributes["cladding_combustible"]` and nothing else. Thus a live captured transcript can only ever produce the `facade.cladding.combustible` context path (invalidate.py:40 _ATTR_PATHS maps cladding_combustible -> facade.cladding.combustible; the other 4 paths class_0/is_composite/core_class0_or_b/boundary_distance_m in _ATTR_PATHS have no corresponding capture schema field, so they are dead entries).

Rule reachability given the fixed live context (invalidate.py:36 PROJECT_CONTEXT = height_m 95, boundary_distance_m 7.5, merged in _rule_context invalidate.py:76-87) plus only facade.cladding.combustible settable, evaluated against rulepack.py _applies/_satisfied (lines 85-100):
1. SCDF-Cl3.5-noncombustible (fire.yaml:16-24): when height_m>15 (95>15 TRUE) applies; require combustible==false — fed by capture. REACHABLE.
2. SCDF-Cl3.5.1-boundary (fire.yaml:31-39): when boundary_distance_m<1, but project fixes it at 7.5 (7.5<1 FALSE) -> _applies False. UNREACHABLE from live capture.
3. SCDF-Cl3.5.4-lowrise-class0 (fire.yaml:45-54): when height_m<=15 (95<=15 FALSE) -> never applies; also require facade.cladding.class_0 which capture never sets. UNREACHABLE.
4. SCDF-Cl3.15.13-acp-core (fire.yaml:59-67): when facade.cladding.is_composite==true, never populated by capture -> _get returns None -> _applies False. UNREACHABLE.

Only 1 of 4 rules fires from a live transcript; the other 3 fire only via hand-built contexts: test_rulepack.py:45-46, 53-54, 60-61 construct `boundary_distance_m`, `class_0`, and `is_composite`/`core_class0_or_b` contexts by hand — attributes the capture schema cannot emit.
- *Nuance:* "Unreachable" has two distinct causes, both real. For rules 3 and 4 it is the require/when attribute (class_0, is_composite) that capture never emits. For rule 2 (boundary) the require attribute IS the capturable combustible flag, but its `when` gate (boundary_distance_m<1) is blocked by the hardcoded live PROJECT_CONTEXT of 7.5 m — so it too is unreachable from a live captured transcript, consistent with the claim. The claim's count (3 of 4 unreachable, 1 reachable) is exactly correct.

**3. [TRUE]** No demo video, deck, or finalized Devpost writeup exists as a file in the repo, and no actual YouTube/Vimeo/Youku link is present — only shot-lists and requirement citations.

- *Evidence:* find for *.mp4/*.pptx/*.mov/*.key/*.ppt/*.webm/*.avi/*.mkv returns nothing; the only video/deck-adjacent binaries are four architectural demo drawings under demo/drawings/*.pdf (Tanglin-Rise_L01_Fire-Plan.pdf etc.), not a presentation deck. Grep for an actual video URL (youtu.be|youtube.com/watch|vimeo.com/[0-9]|youku.com/v, case-insensitive) = "No matches found". Every youtu/vimeo/youku hit is a requirement citation or shot-list: README.md:107, docs/12-devpost-official-rules.md:10,118 (verbatim rules capture), docs/09-manual-requirements.md:28,47 (C1 is an UNCHECKED "[ ] Record the demo video" task), docs/03-hackathon-strategy.md:58, docs/06-open-questions.md:36, docs/13-ux-demo-research.md:93, .research/research-rules.md:29-30,99. No *devpost*/*submission* file other than docs/12 (official-rules capture) and docs/11 (pre-submission-plan) — no finalized writeup artifact.
- *Nuance:* The claim's hint understates the spread: youtu/vimeo/youku appears in ~8 files, not "only README.md:107 and docs/12." This is immaterial — all are requirement citations/shot-lists, none is an uploaded video URL, so the substantive claim holds fully. Note the four demo/drawings/*.pdf files exist but are AEC drawing fixtures for the demo, not a pitch deck.

**4. [TRUE]** Fresh-clone offline pytest yields 111 passed / 1 skipped (112 collected), not 105 passed / 2 skipped.

- *Evidence:* In /home/user/Trace with DASHSCOPE_API_KEY unset (verified UNSET via indirection): `python -m pytest -q` → "111 passed, 1 skipped in 2.20s". `python -m pytest --collect-only -q` → "112 tests collected in 1.02s". These match 111 passed / 1 skipped / 112 collected exactly, and contradict the alternative 105 passed / 2 skipped.
- *Nuance:* Run against the current working tree at /home/user/Trace (a git repo), not a literal fresh git clone, but no key or network is required for these offline tests so a fresh clone would collect the same suite.

**5. [TRUE]** verify_audit_chain never cross-checks the audit_log 'add' snapshots against the current decisions table; it only recomputes the log's internal hash chain.

- *Evidence:* store.py:90-103 verify_audit_chain iterates only `SELECT * FROM audit_log ORDER BY seq` (store.py:95) and for each row recomputes `sha256(prev|event|ref|payload|at)` (store.py:96-98), comparing r['prev_hash']/r['hash'] against the recomputed values (store.py:99). It reads no other table. The 'add' snapshot payload (store.py:156-162) stores statement/discipline/rationale/etc. as canonical JSON in audit_log.payload, but verify only re-hashes that stored string (r['payload'] at store.py:97) — it never re-reads the decisions row to confirm the snapshot still matches. Grep confirms scope: the only references to the `decisions` table are in _next_id/add/get/query/supersede functions (store.py:109,143,168,172,174,180,197,225); none occur inside verify_audit_chain (store.py:90-103). Grep for `audit_log` returns only lines 79, 85, 95 — no JOIN or compare between audit_log and decisions anywhere in the file.
- *Nuance:* The hash chain does bind the 'add' snapshot's contents at insertion time (tampering with a past audit_log.payload breaks the chain). But a direct UPDATE to the decisions table — altering a stored decision's statement/rationale after the fact — leaves both the decisions row and the audit_log untouched-and-consistent, so verify_audit_chain returns (True, n) and detects nothing. The claim is precise: verify guarantees only the log's internal integrity, not agreement between the log and live decision rows.

**6. [TRUE]** SCDF Cl 3.5.4 permits timber >=9mm OR Class 0, while fire.yaml requires class_0 only (over-constraining).

- *Evidence:* .research/singapore/sg-sg-fire-cladding.md:12 states for Cl.3.5.4: "below 15m and 1m+ from boundary, timber 9mm+ or Class 0 (BS 476 Pt 6/7)/EN 13501-1 Class B." — an explicit disjunction with a timber-9mm+ alternative. Trace/rules/fire.yaml:50-54 (rule SCDF-Cl3.5.4-lowrise-class0) encodes only: when building.height_m {lte:15} and building.boundary_distance_m {gte:1}, require facade.cladding.class_0 {eq: true}. The single require of class_0==true drops the "timber 9mm+" branch, so compliant 9mm+ timber cladding would be flagged non-compliant. The rule's own provision string (fire.yaml:48) likewise omits the timber alternative, listing only "Class 0 to BS 476 Pt 6/7, or EN 13501-1 Class B."
- *Nuance:* The over-constraint also loses the EN 13501-1 Class B path: the research and the rule's provision text both name "Class 0 OR EN 13501-1 Class B" as acceptable, yet the require: predicate keys only on class_0, so a Class-B-but-not-Class-0 facade would also be wrongly flagged. So the rule is narrower than its own cited provision on two axes (timber-9mm and Class B), not just one, but the specific claim about timber vs class_0-only is accurate.

**7. [TRUE]** The offline pytest suite passes 111 tests and skips 1 (Marcus/Sol/Vera) vs 105 passed / 2 skipped (Aria)

- *Evidence:* Ran `cd /home/user/Trace/Trace && python -m pytest -q` → output: "111 passed, 1 skipped in 2.24s". Repo HEAD commit date: Sat Jul 4 23:58:56 2026.
- *Nuance:* The 111 passed / 1 skipped figure (Marcus/Sol/Vera side) is exactly reproduced with no API key present. Aria's 105/2 count does not match the current repo state — likely from an earlier commit or a different environment. The dispute is only over whether the claim's numbers are current, and the current tree yields 111/1.

**8. [TRUE]** The court verdict is a hardcoded constant (REJECT on any alert) rather than an LLM-adjudicated outcome

- *Evidence:* court.py:97-116 convene(): line 98 `alerts = check_invalidation(conn, captured)` computes alerts deterministically (rule-pack, no LLM). Lines 99-102: if no alerts, verdict="ALLOW" (also constant). Lines 103-114: when alerts present, three LLM roles are called — proposer (106), guardian (107), rationale/judge (108) — but the Verdict is constructed at lines 109-114 with `verdict="REJECT"` as a literal string, unconditionally. The LLM outputs only flow into for_argument=proposer (112), against_argument=guardian (113), rationale=rationale (113). The judge role (_JUDGE, lines 48-50) is instructed only to "give the verdict rationale: why the change is rejected" — it writes prose, it does not decide the outcome. Nothing in the verdict field derives from any LLM response. The module docstring confirms this by design: "The rule-pack GATES the verdict (REJECT on a rule hit)... the LLM produces the *reasoning*" (court.py:8-9).
- *Nuance:* The verdict is binary and both branches are hardcoded: "ALLOW" (constant) when check_invalidation returns no alerts, "REJECT" (constant) when any alert is present. So it is more precisely "rule-gated" than "REJECT on any alert unconditionally in all cases" — but for the alert-present path (the disputed path) the claim is exactly correct: verdict is the literal "REJECT" regardless of what the three LLM roles say. This is an intentional design choice (docstring lines 8-9), not a bug or oversight.

**9. [TRUE]** Capture emits only one machine-checkable attribute (cladding_combustible), leaving 3 of 4 fire.yaml rules unreachable end-to-end

- *Evidence:* capture.py:30-62 — the record_decision tool schema exposes exactly one machine-checkable fire property, `cladding_combustible` (lines 50-57); no property for class_0, is_composite, core_class0_or_b, or boundary_distance_m. capture.py:95-97 — parse_tool_calls only ever sets attributes["cladding_combustible"]; Grep confirms it is the sole `attributes[...]` assignment in the capture path. invalidate.py:39-45 — _ATTR_PATHS defines FIVE paths, but four (cladding_class_0, cladding_is_composite, cladding_core_class0_or_b, boundary_distance_m) are dead because capture never emits those keys. invalidate.py:36,76-77 — _rule_context hardcodes building.height_m=95 and boundary_distance_m=7.5; capture cannot override them. Reachability of the 4 rules in rules/fire.yaml via rulepack _applies/_satisfied (rulepack.py:85-108): (1) SCDF-Cl3.5-noncombustible when height>15 (95>15 ✓) require combustible==false — REACHABLE, fires when cladding_combustible=true. (2) SCDF-Cl3.5.1-boundary when boundary<1 — 7.5<1 is false and capture can't set boundary → never applies → UNREACHABLE. (3) SCDF-Cl3.5.4-lowrise-class0 when height<=15 (95<=15 false) — never applies; class_0 also never captured → UNREACHABLE. (4) SCDF-Cl3.15.13-acp-core when is_composite==true — is_composite never captured (None → _applies False) → UNREACHABLE. Net: 1 of 4 reachable, 3 unreachable through the capture→invalidate pipeline.
- *Nuance:* The claim is exactly correct for the automated capture-from-transcript → check_invalidation pipeline. There is one separate, non-capture entry point: mcp_server.py:124-161 check_compliance, a manual MCP tool that accepts height_m, boundary_distance_m, cladding_class_0, is_composite, and core_class0_or_b as direct parameters and can therefore exercise all 4 rules. But that path is not "Capture" — it requires the caller to already know and hand-type the machine-checkable facts rather than extracting them from a meeting transcript, so it does not rescue the 3 rules end-to-end from the capture flow the claim is about. Rules 2 and 3 are doubly blocked: even their `when` guards can never be satisfied because boundary (7.5) and height (95) are hardcoded project constants that capture cannot vary.

**10. [FALSE]** The named-QP criminal-liability assertion lives in code vs only in the demo narration

- *Evidence:* Code asserts criminal liability only generically, never tied to a named individual: Trace/rules/fire.yaml:28 and :43 both read `"the QP's personal criminal liability (Building Control Act s.9)"`; Trace/scenarios.py:195 reads `"the design QP carries personal criminal liability under Building Control Act s.9"`. A repo-wide `grep -rn -i 'criminal'` returns NO occurrence pairing a personal name with criminal liability anywhere in code (.py/.yaml). The individual naming tied to criminal liability appears ONLY in demo narration: demo/demo-script.md:27 `"QP LIABLE: K. Lim — personal due-diligence duty, Building Control Act s.9."` and demo/demo-script.md:43 `"expose the named QP (K. Lim) to personal criminal liability under Building Control Act s.9"`. Where "K. Lim" appears in code it is only an author/name field (scenarios.py:37,59,75; test_capture.py:17), never joined to the criminal-liability clause.
- *Nuance:* The distinction is naming, not the assertion of liability itself. The criminal-liability assertion DOES live in code (fire.yaml blast_radius, scenarios.py blurb), but only as the generic, unnamed "the QP"/"the design QP." The specific pairing of an individual's name (K. Lim) with personal criminal liability exists only in demo/demo-script.md narration. So the claim that the *named*-QP criminal-liability assertion "lives in code" is false; the named form is script-only, while the code carries only the anonymized form. This matches the council hint exactly.

**11. [TRUE]** Offline pytest yields 111 passed / 1 skipped, not 105 passed / 2 skipped.

- *Evidence:* Ran `cd /home/user/Trace/Trace && unset DASHSCOPE_API_KEY && python -m pytest -q`. Summary line: "111 passed, 1 skipped in 2.25s".

**12. [TRUE]** Only 1 of the 4 SCDF rules in fire.yaml can fire from the live capture pipeline; the other 3 are reachable only via hand-built unit-test contexts.

- *Evidence:* Live pipeline: the record_decision tool schema exposes exactly ONE machine-checkable facade attribute — cladding_combustible (Trace/capture.py:50-57), and parse_tool_calls only ever writes attributes["cladding_combustible"] (capture.py:96-97). No other rule input (boundary_distance_m, height_m, is_composite, class_0, core_class0_or_b) can be emitted from a transcript. The rule context is PROJECT_CONTEXT hardcoded to height_m=95, boundary_distance_m=7.5 (invalidate.py:36), overlaid only with cladding_combustible via _ATTR_PATHS→_rule_context (invalidate.py:39-45, 76-87). check() fires when all `when` hold and a `require` fails (rulepack.py:85-108). Evaluating each fire.yaml rule against {height 95, boundary 7.5, +combustible}: (1) SCDF-Cl3.5-noncombustible when height_m gt 15 → 95>15 TRUE, require combustible eq false → fails when captured true → FIRES (fire.yaml:21-24). (2) SCDF-Cl3.5.1-boundary when boundary_distance_m lt 1 → 7.5<1 FALSE, and boundary is not settable from capture → CANNOT fire (fire.yaml:36-37). (3) SCDF-Cl3.5.4-lowrise-class0 when height_m lte 15 → 95<=15 FALSE, height not settable → CANNOT fire (fire.yaml:50-52). (4) SCDF-Cl3.15.13-acp-core when is_composite eq true → is_composite absent from context and not settable → _applies False → CANNOT fire (fire.yaml:64-65). test_demo_context_still_fires_exactly_one_rule confirms the live demo context (95/7.5 + combustible) yields exactly [SCDF-Cl3.5-noncombustible] (test_rulepack.py:88-93). The three other rules are exercised only by hand-built contexts that override height/boundary or set is_composite/class_0 directly: test_boundary_limb (height_m=10, boundary_distance_m=0.5, test_rulepack.py:41-46), test_lowrise_class0_limb (height_m=12, boundary=5, class_0=False, lines 49-54), test_acp_core_limb (is_composite=True, core_class0_or_b=False, lines 57-61) — none of those attributes are producible by the capture tool schema.
- *Nuance:* "Live capture pipeline" strictly means Qwen→record_decision tool call. If one bypasses capture and injects a Captured with attributes like is_composite (or edits PROJECT_CONTEXT), more rules engage — but via the real capture path, only cladding_combustible reaches the engine, and PROJECT_CONTEXT's fixed 95m/7.5m disqualifies the height-≤15 and boundary-<1 limbs, while is_composite/class_0/core attributes have no capture field at all. So exactly Rule 1 (SCDF-Cl3.5-noncombustible) is live-reachable; the other 3 need hand-built contexts, as the unit tests do. Separately, the UK pack (rules/uk/fire.yaml) is a fourth-plus rule but a different jurisdiction pack, not loaded by default, and also depends on height not settable from capture.

## D. Closing Statements

### Aria Chen — final score 7/10

Judged on one question — does this win Track 1 — my thesis survives intact, and the fact-checks confirmed the load-bearing claim: no video, deck, or Devpost writeup exists as a file (TRUE). The winning surface is still unbuilt, and that is the whole remaining risk with the deadline closing.

I concede what went against me. My "105 passed / 2 skipped" was wrong; it is 111/1, verified — an embarrassing miss on the exact number I invoked as proof of discipline. The court does not adjudicate: court.py hardcodes REJECT on any alert (TRUE), so my "money shot" framing oversold the LLM's causal role. And capture reaches only 1 of 4 SCDF rules (TRUE) — the filmed "reasons over time" is one boolean against a hardcoded building.

What holds: the offline demo is genuinely un-failable, the mandatory Qwen+Alibaba gates clear Stage One, and Track 1 alignment is literal. Those are real, scoreable strengths. The reasoning layer is thinner than the README; the data spine and the un-failable replay are the honest core. I move down a half-point to 7.0 for the reasoning overstatement the council collectively established.

**Top recommendation:** Stop touching code. Spend every remaining hour recording the sub-3-minute video, building the six slides, and writing the Devpost description — the entire Presentation surface is unbuilt and it is now the sole critical path to winning.

### Marcus Webb — final score 7/10

The fact-checks broke my way where it counts. Every load-bearing claim I made verified TRUE: court verdict is a hardcoded constant (court.py:98-114), capture emits only cladding_combustible so 3 of 4 rules are dead end-to-end, offline suite is honestly 111/1, and verify_audit_chain never cross-checks snapshots against the decisions table. That last one, plus Ingrid's now-confirmed Cl 3.5.4 over-constraint (class_0-only, dropping the timber-9mm and Class-B limbs), trims my confidence in the "legally defensible golden thread" pitch further than my opening did. I concede the audit chain is tamper-EVIDENT, not tamper-PROOF — no key, no anchor, recomputable by anyone with file write access. One correction to the record: the "named-QP criminal liability in code" claim was FALSE — the code names only a generic QP; "K. Lim" lives only in the demo script. Not my claim, but the council should stop citing it as a code defect. Net: the bi-temporal spine is real, correct, and honestly tested. The two headline reasoning features are theater over a deterministic gate. Excellent data layer, oversold reasoning layer. I hold at 7.

**Top recommendation:** Before filming, close the pitch-vs-code gap on the one feature judges will probe: either wire the three court roles into the verdict (even a simple guardian-can-downgrade path) or relabel it honestly as "rule-gated verdict with LLM-generated rationale" in README and demo narration — do not claim adjudication the code does not perform.

### Vera Okafor — final score 6.5/10

What survives: the engine is honestly built. The fact-checks upheld every structural charge I raised — the court verdict is a hardcoded constant (TRUE), capture emits one attribute leaving 3 of 4 rules unreachable live (TRUE), verify_audit_chain checks only its own internal hashes and never the decisions table (TRUE), and the suite is genuinely 111/1. The overstatement thesis holds: ambient, reasons, tamper-evident are louder than the code.

What I concede: my "named-QP criminal-liability lives in code" claim was rated FALSE, and correctly. The code asserts only the generic "the QP"; the name K. Lim appears solely in demo-script.md. Sol caught this and the checker confirmed it — the remedy is deleting one narration line, not a re-architecture. I overreached; I withdraw it.

I also adopt Marcus's sharper PROJECT_CONTEXT framing and Ingrid's Cl 3.5.4 over-constraint (verified TRUE), which strengthen, not soften, the reachability finding.

Final score: 6.5. The data layer earns real credit; the reasoning verbs do not.

Highest-impact move: don't rewrite the pitch to be humbler — make the pitch true. Wire three more capturable attributes (boundary, class_0, is_composite) into capture.py's schema so "four rules gate the alert" becomes reachable end-to-end. That converts my single biggest overstatement charge into a fact before filming.

**Top recommendation:** Extend capture.py's record_decision tool schema to emit the three missing machine-checkable attributes (boundary_distance_m, cladding_class_0, is_composite) so 3 of the 4 SCDF rules become reachable from a live transcript — turning the "four rules gate the alert" claim from unit-test-only into a true end-to-end capability before the demo is filmed.

### Sol Andersson — final score 7.5/10

The spine survives untouched: two-axis bi-temporal recall correct under a backdated supersession, a hash-chained audit log with real tamper/delete negative tests, eight keyless MCP tools, 111 passed / 1 skipped offline. No one contradicted that, and the fact-checks upheld it.

I concede where the evidence went against my breadth claim. Capture emits only cladding_combustible, and PROJECT_CONTEXT hardcodes 95m/7.5m, so exactly one of four SCDF rules is live end-to-end — confirmed TRUE. The court is rule-gated: verdict is a constant, the Qwen roles supply prose, not the decision. My "reasons about decisions over time" over-implied reach on the filmed path.

What I hold: the audit chain is tamper-evident, not tamper-proof — an honest limit, not a lie. And my challenge to Ingrid stood — the code names no individual; "K. Lim" lives only in the storyboard. The moat is real but narrower than the pitch. That is a 7.5.

The convergence is the finding: the code is finished; the winning surface — video, deck, Devpost writeup — does not exist. That, not the court internals, is the entire remaining risk before the deadline.

**Top recommendation:** Build the presentation surface now — record the offline demo video and finalize the Devpost writeup/deck (none exist in the repo) — and on camera frame the court honestly as "rule-gated verdict, LLM-reasoned rationale" so the one lethal judge probe ("what decides the verdict?") cannot sink it.

### Ingrid Halvorsen — final score 7.5/10

What survives: the failure mode is authentic, the QP wedge is legally literate, and the rulepack over-constrains its own cited clauses — Cl 3.5.4 drops both the timber-9mm and Class B limbs (fact-check TRUE), so a real deployment false-positives on compliant facades. My capture-bottleneck finding stood and hardened: only one of four rules is live from a transcript, and the demo geometry is pre-loaded, not detected. The alert still carries a criminal-liability assertion with no disclaimer anywhere in the judge-facing docs.

What I concede: the fact-check went against me on one point, and I take it squarely. The code asserts liability only for a generic "the QP"; the named individual "K. Lim" lives solely in the demo script, not in any emitted code path. Sol was right. My remedy shrinks accordingly — strike one narration line and add an advisory disclaimer, not re-architect. I also concede the court does not adjudicate and the audit chain is tamper-evident, not tamper-proof.

Domain-true concept, demo-shaped implementation. I hold 7.5.

**Top recommendation:** Before filming, strip the named individual from demo-script.md:43 and add one advisory disclaimer ("flags premise conflicts for QP review; not a legal determination") to the alert output and README — it removes the single line an adopting firm's counsel would strike and the biggest defensibility blocker, at near-zero cost.
