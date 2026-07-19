---
tags: [pillar]
---

# Timely forgetting of outdated information

Track 1's second stated focus, and Trace's differentiator: **active
premise-invalidation**. The moment a new decision contradicts an earlier
one's premise, that earlier decision is superseded (never deleted), and a
[[Decision Court]] convenes to argue and record the verdict.

This pillar got materially stronger this update: the verdict is no longer
just a printed sentence — REJECT and ALLOW are now real state transitions
on the record (adopt / reject / auto-link a supersession), so "timely"
forgetting actually happens in the data, not just in the demo narrative.

## Implemented by

- [[Invalidation Alert]] — names the specific stored assumption broken.
- [[Rule-pack (SCDF)]] — the deterministic gate that keeps the alert reliable.
- [[Decision Court]] — Proposer, Guardian, Judge argue it out, and the
  verdict now adopts/rejects/supersedes for real.
- [[Decision Store]] — supersession closes `valid_to`, links `superseded_by`.

## Related

- [[Trace]]
