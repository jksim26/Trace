---
tags: [module]
source: Trace/vault_watcher.py
---

# Vault Watcher

The knowledge base's intake, wired to the full pipeline — one working
answer to "does Trace actually listen automatically?" Polls
`kb/<project>/inbox/` (the same poll-and-dedupe shape [[Desktop Watcher]]
uses on window titles, but on files): drop a markdown meeting note into the
inbox and, unprompted, Trace (1) stores it verbatim as an immutable,
audit-chained *episode*, (2) runs [[Capture]] on it (Qwen function-calling),
(3) checks every capture against the project's [[Rule-pack (SCDF)]] and the
LLM premise check via [[Invalidation Alert]], (4) convenes [[Decision Court]]
on a conflict — the verdict lands as a real state transition — and (5)
re-exports the [[Knowledge Base Vault]] so the note's consequences are
immediately visible in the graph.

Loop-guarded both ways: notes whose frontmatter says `generated-by: trace`
are projections and are never re-ingested (sources and projections stay
one-way), and a note whose frontmatter names a *different* project is
skipped (dropped in the wrong inbox). Dedupe is content-addressed — re-saving
identical text is a no-op. A note's own `date:` frontmatter becomes the
decision's `valid_from`; ingestion time stays `recorded_at` — the same
bi-temporal honesty [[Bi-temporal Time-Travel]] depends on elsewhere.

This is a *file-based* "listens automatically," distinct from (and
complementary to) an audio-based one: it watches for a note being dropped
into a folder, not a live meeting being recorded. It has no dedicated test
file yet — the newest and most complex module in this update without one.

## Related

- Feeds [[Decision Store]] via [[Capture]], [[Invalidation Alert]], [[Decision Court]].
- The write path into the [[Knowledge Base Vault]] (inbox in, projections out).
- Same allowlist/poll philosophy as [[Desktop Watcher]] and [[Ambient Trigger]],
  applied to files instead of window titles.
