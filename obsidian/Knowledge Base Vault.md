---
tags: [module]
source: Trace/kb.py
---

# Knowledge Base Vault

Trace's second brain as a plain markdown vault (`kb/`). Renders the whole
[[Decision Store]] out as Obsidian-compatible notes: `kb/<project>/decisions/`,
`kb/<project>/court/`, and `kb/<project>/episodes/` are **projections** —
regenerated from the store after every write, never read back — plus a
per-project `_index.md` and an `inbox/` drop zone that [[Vault Watcher]] owns.

Every generated note carries a `record_sha256` of the underlying row, so
`verify_vault()` can re-render the expected note and diff it against disk —
catching a manually edited projection the same way `verify_audit_chain`
catches an altered log entry (see [[Golden Thread]]). Filenames equal
decision ids, so `[[<id>]]` wikilinks resolve and Obsidian's Graph View
*is* the decision graph — supersession chains, court verdicts, evidence
links — with no dependency on Obsidian itself: it's still just a folder of
markdown, readable in any editor. Frontmatter follows the MADR/ADR
convention (a `status` lifecycle field, explicit `superseded_by`/`supersedes`
links). Keyless and deterministic — no LLM, no network.

## Related

- Reads from [[Decision Store]] and [[Decision Court]]'s persisted records.
- The one-way counterpart to [[Vault Watcher]] (sources go in via `inbox/`,
  projections come out via `decisions/`/`court/`/`episodes/` — never both
  for the same file).
- Extends [[Golden Thread]] to the markdown layer.
