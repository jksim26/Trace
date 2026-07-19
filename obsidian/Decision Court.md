---
tags: [module]
source: Trace/court.py
---

# Decision Court

Three Qwen roles — Proposer, Guardian, Judge — deliberate a conflict, write
the reasoning a personally-liable QP can stand behind, and persist every
verdict to the court record. Scene 2 of the [[CLI Demo]] (the REJECT
verdict; the rejected proposal is preserved, never deleted).

**Verdicts are now real state transitions, not just prose.** REJECT actually
marks the proposal `rejected` on the record; ALLOW actually adopts it as
`valid` and, if it genuinely displaces an in-force decision, automatically
links that decision as `superseded` — no separate manual step needed.

**Evidence is treated differently depending on its source:** a [[Rule-pack
(SCDF)]] violation is deterministic law — the verdict is always REJECT, and
the LLM only writes the reasoning (reliable on camera). An LLM premise-check
alert is probabilistic evidence — here the Judge genuinely decides ALLOW or
REJECT after hearing both sides (an unparseable ruling falls back to REJECT,
the conservative default for a QP's record).

## Related

- Convened by [[Invalidation Alert]].
- Gated by [[Rule-pack (SCDF)]] (only for deterministic rule hits).
- Persists verdicts to, and adopts/rejects/supersedes directly on, [[Decision Store]].
- Read by [[Ambient Bubble]]'s chat and rendered into the [[Knowledge Base Vault]].
- Implements [[Timely Forgetting]].
