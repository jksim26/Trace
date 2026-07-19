---
name: verify
description: Build/launch/drive recipe for verifying Trace changes at their real surfaces (bubble HTTP, vault_watcher CLI, MCP stdio).
---

# Verifying Trace

Deps: `pip install pyyaml python-dotenv openai` (plus `mcp` for the MCP
server, `qwen-agent numpy soundfile` only for mcp_tools). All commands run
from `Trace/`.

## Surfaces

- **Bubble (HTTP)**: `TRACE_DB_DIR=<tmp> TRACE_PORT=8899 python bubble.py
  --no-browser`, then `curl --noproxy '*' http://127.0.0.1:8899/state` and
  POST `/ask` with `{"question": ..., "project": ...}`. Without an API key,
  `/ask` degrades to the deterministic abstention — that is expected, not
  a failure.
- **Vault watcher (CLI)**: `python vault_watcher.py <project>` polls
  `kb/<project>/inbox/` and seeds `kb/<project>/trace.db` next to it. Its
  kb root is fixed to the repo's `kb/` — to avoid touching the working
  tree, copy the repo somewhere disposable and run the CLI there.
  Ingesting a real note needs DASHSCOPE_API_KEY (capture is LLM-driven);
  the guard paths (projection notes, wrong-project notes, unknown project)
  need no key.
- **MCP (stdio)**: drive `python mcp_server.py` with an `mcp` SDK
  stdio_client; tool results are JSON in `content[0].text`.

## Shared persistent store

All three surfaces open the same `kb/<project>/trace.db`
(`scenarios.open_store`; seeded on first open). `TRACE_DB_DIR=<tmp dir>`
redirects it — always set it when driving bubble/MCP so runs stay isolated
and repeatable. Delete `trace.db*` to reset to the demo seed.

## Gotchas

- This environment routes HTTP through a proxy: local curl needs
  `--noproxy '*'`.
- Don't `pkill -f` a pattern that appears in your own command line — it
  kills the invoking shell.
- Tests (`python -m pytest -q`) already isolate TRACE_DB_DIR via
  conftest.py; expected: all pass, 2 skipped (need real key / mcp pkg).
