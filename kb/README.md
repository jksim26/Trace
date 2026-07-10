# kb/ — Trace's second brain (a plain markdown vault)

This folder is Trace's knowledge base: one folder per project, readable in any
editor. Point Obsidian at `kb/` and **the graph view is the decision graph** —
supersession chains, court verdicts and source episodes appear as linked notes,
because filenames equal decision ids and every relationship is a `[[wikilink]]`.
Nothing here *requires* Obsidian: it is just markdown with YAML frontmatter
(the frontmatter follows the MADR / ADR convention — a `status` lifecycle field
plus explicit `superseded_by` / `supersedes` links).

## The one rule: sources in, projections out — never both

| Folder | Direction | What it is |
|---|---|---|
| `<project>/inbox/` | **source → Trace** | The drop zone. Put a markdown meeting note here and the vault watcher ingests it: stored verbatim as an immutable, audit-chained **episode**, decisions captured with rationale + assumptions, checked against the project's rule-pack and the LLM premise check, court convened on a conflict. |
| `<project>/decisions/` | **Trace → projection** | One note per decision, regenerated from the store after every write. **Do not edit** — the SQLite store (with its SHA-256 hash-chained audit log) is the record; these notes are views of it. Each carries a `record_sha256`; `kb.verify_vault` detects any edited or stale projection. |
| `<project>/court/` | Trace → projection | One note per decision-court verdict, linking the judged proposal and the decision it broke. |
| `<project>/episodes/` | Trace → projection | The ingested source notes, re-rendered with their content hash — readable provenance for every `source_episode` reference. |
| `<project>/_index.md` | Trace → projection | The project's decision register as a table. |

Commentary belongs in your own notes: link `[[408213-D-001]]` from anywhere in
the vault and Obsidian's backlinks pane attaches your note to the decision —
without touching the record.

## Try it

```bash
cd Trace
python kb.py                        # regenerate the whole vault (keyless, offline)
python vault_watcher.py pearl-vista # watch the inbox (capture needs DASHSCOPE_API_KEY)
# now drop a meeting note into kb/pearl-vista/inbox/ and watch the court convene
```

Note frontmatter the watcher understands: `date:` (becomes the decision's
`valid_from` — ingestion time stays `recorded_at`, the bi-temporal "what did
you know, and when"), and `generated-by: trace` marks a projection the watcher
must never re-ingest.
