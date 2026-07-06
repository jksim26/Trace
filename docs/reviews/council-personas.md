# The Trace Review Council — Personas & How to Reconvene

*First convened 2026-07-02 ([full verdict](2026-07-02-council-review.md) · overall 6.5/10); reconvened 2026-07-06 ([Round 2](2026-07-06-council-review.md) · overall 7.0/10, +0.5). The council is five AI reviewers with deliberately opposing mandates, an independent fact-check bench, and a presiding judge. Saved here so the same panel can be re-invited to judge the project's improvement.*

## The process

1. **Opening statements** — all five members independently read the entire repo (code, tests, docs, demo, research) and stake 3–6 falsifiable claims each.
2. **Rebuttals** — each member reads all openings and challenges colleagues' claims by name, with file:line evidence; concessions are recorded.
3. **Fact check** — every factual claim the council disputes goes to an independent verifier who rules TRUE / FALSE / PARTIAL against the actual code.
4. **Closing statements** — final positions and scores after the fact-checks land.
5. **Verdict** — the presiding judge weighs argument quality (not score averages), rules on each disagreement, and issues the scorecard + ranked recommendations.

## The members

### Aria Chen — The Hackathon Judge
Has judged dozens of AI hackathons. Evaluates only one question: *will this win Track 1?* Rubric alignment, demo punch for a tired judge watching 100 entries, differentiation vs "chatbot + vector DB" entries, whether remaining scope is finishable, single-point-of-failure demo risks, whether the pitch materials land.
*Round 1: opened 8/10 → closed 7/10.*
*Round 2 (2026-07-06): opened 7.5/10 → closed 7/10. Conceded the stale 111/1 test count and the "money shot" overselling of the court's LLM role.*

### Marcus Webb — The Staff Engineer
Twenty years of code review; unimpressed by pitches, only trusts code. Runs the test suite the way a fresh judge would. Hunts real defects: temporal-query correctness, ID collisions, timestamp fragility, happy-path-only tests, fresh-clone installability. Scores the code as code.
*Round 1: opened 5.5/10 → closed 6/10. Won the bi-temporal dispute.*
*Round 2: opened 7/10 → closed 7/10 (+1). Conceded the bi-temporal fix is genuine; won "the court verdict is a hardcoded constant" and "only 1 of 4 rules fires end-to-end."*

### Vera Okafor — The Skeptic
Professional debunker. Audits the gap between what the pitch claims and what the code does, claim by claim, with file:line evidence — and explicitly credits the claims that are honest, because a skeptic who only attacks loses credibility in the debate.
*Round 1: opened 5.5/10 → closed 5/10. Won the pitch-honesty dispute.*
*Round 2: opened 6.5/10 → closed 6.5/10 (+1.5 — the largest jump; the pitch-vs-code gap narrowed most). Surfaced the audit-chain-vs-decisions-table gap; overreached once (named-QP liability lives in narration, not code) and withdrew cleanly.*

### Sol Andersson — The Champion
Steelman advocate. Argues the strongest honest case for the project, anchored to specific files/lines so it survives cross-examination, and concedes undeniable weaknesses preemptively.
*Round 1: opened 8/10 → closed 7/10.*
*Round 2: opened 8/10 → closed 7.5/10. Won the "named-QP criminal liability lives only in the storyboard, not the code" dispute — the one place a skeptic overreached.*

### Ingrid Halvorsen — The AEC Domain Expert
Thirty years across architecture practice and building-compliance consulting. Judges domain truth: does the failure story match how AEC actually fails, are the fire rules faithful to their cited clauses, do the transcripts read real, are the golden-thread and QP-liability wedges legally sound, what would a real firm need to adopt.
*Round 1: opened 7/10 → closed 6/10. Found the missing 1m-boundary limb in fire.yaml.*
*Round 2: opened 8/10 → closed 7.5/10. Found the Cl 3.5.4 over-constraint (fire.yaml requires class_0 only, dropping the timber-9mm and Class-B limbs) and the undisclaimed liability-conclusion gap in the alert.*

### The Presiding Judge
Does not review the repo first-hand except to break ties. Weighs the debate record, rules on every disagreement using the fact-check verdicts, refuses to average scores mechanically, and issues the scorecard, the list of claims that failed fact-checking, and the top-5 ranked recommendations.

## How to reconvene the council

The full panel is scripted at [`.claude/workflows/council-review.js`](../../.claude/workflows/council-review.js). In a Claude Code session on this repo, ask to *"reconvene the council"* — or invoke the workflow directly:

```
Workflow({
  name: 'council-review',
  args: {
    today: '<today's date>',
    priorReview: 'docs/reviews/2026-07-02-council-review.md',   // enables re-review mode
    focus: 'Judge the improvement: were the top-5 recommendations executed?'  // optional
  }
})
```

With `priorReview` set, every member reads the previous verdict first and must explicitly compare: which recommendations were executed, whether previously-FALSE claims are now true or removed, and what regressed. The judge's report gains an **"Improvement since the last review"** section with a justified score delta.

Save each new verdict alongside the previous ones in `docs/reviews/` (dated filename) so the series tracks the project's trajectory.
