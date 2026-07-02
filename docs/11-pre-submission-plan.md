# 11 · Pre-Submission Fix Plan — July 2 → 7

*Drafted 2026-07-02 from the council review ([docs/reviews/2026-07-02-council-review.md](reviews/2026-07-02-council-review.md)), the judging rubric in [03-hackathon-strategy.md](03-hackathon-strategy.md) (Technical Depth 30% · Innovation 30% · Problem Value 25% · Presentation 15%), and direct inspection of the code. Internal target **7 July**; hard deadline **9 July, 14:00 PDT**.*

---

## The strategy in one paragraph

The concept (8/10) and domain story (8/10) are already contest-winning — don't touch them. The score is dragged by three things a judge hits in their first ten minutes: a **broken fresh-clone install**, a **pitch that claims three components the code doesn't have** (hybrid retrieval, LLM premise check, MCP tools), and a **flagship "bi-temporal" query with a reproducible hole**. All are cheap to fix relative to their scoring impact. The plan: *make the pitch true* (build the claimed thing or delete the claim), *make the judge's first ten minutes flawless*, and only then spend time on features. Doc 03 §8 already says it: "a credible team scores higher than an overclaiming one."

---

## Day 1 — **Wed 2 July**: stop the bleeding (~4–6h)

The judge's first two actions are `pip install && pytest` and reading the Devpost text. Both currently fail.

1. **Fix the fresh-clone path.** Add `pyyaml`, `numpy`, `soundfile`, `python-dateutil` to `Trace/requirements.txt` (pyyaml is a *direct* dependency of rulepack.py; the others are undeclared qwen-agent needs). Verify in a clean venv.
2. **Make bare `pytest` collect green.** Guard `test_connection.py` with `pytest.mark.skipif(not os.getenv("DASHSCOPE_API_KEY"), ...)` so it skips instead of erroring at collection.
3. **The truth pass** over README.md, docs/10-pitch-kit.md, demo/demo-script.md:
   - "hybrid retrieval (text-embedding-v4 + BM25 + qwen3-rerank)" → describe what ships ("deterministic keyword retrieval packed to a token budget") *unless* the Day-3 embedding-hybrid stretch is committed to — decide now which.
   - "MCP tools" → "Qwen-Agent custom tools" (mcp_tools.py has no MCP protocol code — it is `@register_tool`).
   - One measured test count everywhere (currently 33 vs 36 vs actual 46).
   - "immutable audit trail" → "never-delete, append-only by design" (supersession is a SQLite UPDATE — don't hand a sharp judge that word).
   - demo-script.md:82 claims Scene 2 shows "the supersede chain" — cli.py never calls `supersede_decision`; align the script with what's on screen.
4. ~~**Human task, do it today:** verify the live Devpost rules.~~ **DONE 2026-07-02** — verbatim capture in [12-devpost-official-rules.md](12-devpost-official-rules.md). Key rulings: video **< 3 min**; **Alibaba Cloud deployment MANDATORY** (proof = a repo code file demonstrating Alibaba Cloud services/APIs); architecture diagram required; license visible in the GitHub About section; a working testing-access link required through 31 Jul.

## Day 2 — **Thu 3 July**: fix the flagship defect (Technical Depth 30%) (~4–6h)

1. **Patch `get_valid_asof`** (store.py:131-138): the query never reads `superseded_at`, so a retroactively backdated supersession makes "what did we know on Feb 15" return nothing — and retroactive recording is the AEC norm. Roughly a two-predicate fix: knowledge axis `(superseded_at IS NULL OR superseded_at > ?)`, and treat `valid_to` as open when the supersession wasn't yet known: `(valid_to IS NULL OR valid_to > ? OR superseded_at > ?)`.
2. **Add the regression test** for exactly that scenario (record Jan 1 → supersede Mar 1 backdated to Feb 1 → query as-of Feb 15). This turns the worst fact-check finding into the best demo beat: *"what did you know, and when."*
3. **Sweep the other confirmed defects**, all small:
   - `recall.py:99` returns `candidates` hardcoded to `0` on abstention — return the real count (one token).
   - `_next_id`'s `COUNT(*)` collides after any deletion/re-import — use `MAX(id)+1`.
   - Guard `supersede_decision` against double-supersede (raise if `old.status == 'superseded'`).

## Day 3 — **Fri 4 July**: make the differentiator real (Innovation 30%) (~6–8h)

The product is named for premise-invalidation, but `check_invalidation` never reads the stored `assumptions` — it picks `same_discipline[-1]` positionally, and the "LLM premise check" promised in invalidate.py:5 and *claimed as built* in docs/10:45 doesn't exist.

1. **Build the LLM premise check** — the highest-value feature-hour of the week. For each currently-valid decision, have qwen-max compare the new decision against that decision's stored `assumptions` and return which premise breaks. Keep the rulepack as the deterministic *gate* for the demo alert (that design is correct — the council's compliance expert defended it), with the LLM as the general path — exactly what the docs already promise.
2. **Pick `breaks` by the actually-conflicting premise**, not list position.
3. **Deepen fire.yaml from 1 rule to 3–4** — starting with the 1m-boundary limb of SCDF Cl 3.5 that `.research/` records but the YAML omits.
4. **Persist court verdicts** (court.py currently discards them) so the "defensible record" the court narrates actually exists in the store.
5. *Stretch — cut first if behind:* honest hybrid retrieval = keyword score + text-embedding-v4 cosine. Skip BM25/rerank; either build this or keep the Day-1 de-claim.

## Day 4 — **Sat 5 July**: demo resilience + deploy insurance (~4–6h)

1. **Add a no-key/replay mode to cli.py.** The happy path makes ~6 live DashScope calls with no fallback and crashes at Scene 1 without a key. Record the LLM responses once, replay with `--offline` — protects the video shoot, any live-demo request, and every judge without credentials.
2. **Deploy to Alibaba Cloud — now confirmed MANDATORY** (rules §4, see doc 12): the backend must run on Alibaba Cloud, with proof being *a link to a repo code file that demonstrates use of Alibaba Cloud services/APIs*. The deployed instance also doubles as the required **testing-access link** (free access through 31 Jul). Make sure a clearly-named code file shows the Alibaba Cloud usage.
3. **Feature freeze at end of day.** Full clean-clone test on Windows and Linux.

## Day 5 — **Sun 6 July**: packaging (Presentation 15% + the submission itself)

- Record + edit the **< 3-min video** (pre-recorded happy path; no copyrighted music/trademarks — rules §4).
- **Architecture diagram** (docs/02 §8 is still ASCII) — a required submission item, not polish.
- **Deck** and **Devpost write-up** — include the "significantly updated during the Submission Period" explanation the rules ask for.
- **Blog post (optional but cheap):** a public build-journey post with Qwen Cloud, linked in the submission — separate 10 × ($500 + $500) prize pool.
- Confirm GitHub shows the MIT license in the repo's **About section** (an explicit rules requirement).
- Run the council's fact-check table (§5 of the review) as a literal pre-flight checklist: every judge-facing sentence verified against the code that day.

## Day 6 — **Mon 7 July**: **SUBMIT.**

**8–9 July stay pure buffer — plan zero work there.**

---

## Where the points come from

| Fix | Rubric bucket | Why it moves the score |
|---|---|---|
| Fresh clone + truth pass (Day 1) | All of them | Removes the two instant-credibility-killers in the judge's first 10 minutes |
| `get_valid_asof` + defect sweep (Day 2) | Technical Depth 30% | The flagship claim becomes demonstrably true, with the regression test as proof |
| LLM premise check + deeper rulepack (Day 3) | Innovation 30% | The differentiator generalizes beyond one hardcoded scenario; "sophisticated Qwen use" becomes real |
| Replay mode + deployment (Day 4) | Presentation + qualification | The demo cannot fail on camera; deployment clause covered either way |
| Video/diagram/deck (Day 5) | Presentation 15% | These deliverables don't exist yet and are submission requirements |

## The cut-line if the schedule slips

Days 1–2 are **non-negotiable**. Day 3's premise check is the one feature worth fighting for. Cut in this order: embedding hybrid → bubble polish → extra fire.yaml rules.
