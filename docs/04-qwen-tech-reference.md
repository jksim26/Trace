# 04 · Qwen Cloud Build Reference

*Practical reference for building on the required stack. All figures **`[web search]` / vendor-doc unless tagged `[verified]`** — re-confirm against the live Model Studio console before hard-coding, as 2026 model specs move fast.*

---

## 1. Platform map

- **Model Studio** (English) = **Bailian / 百炼** (Chinese) = the platform you build on.
- **DashScope** = the API/SDK surface. Get your API key from the Model Studio console.
- Two ways to call:
  1. **Native DashScope SDK** — `pip install dashscope` (Python/Java); fullest feature set.
  2. **OpenAI-compatible endpoint** — reuse the OpenAI SDK; just swap key + base_url + model name. *(Recommended for speed — most agent libraries work unchanged.)*

### Endpoints `[verified — Model Studio doc]`
| Region | OpenAI-compatible base URL |
|---|---|
| **International (Singapore) — use this** | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| Singapore — new per-workspace form | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| China (Beijing) | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

The **free hackathon quota lives on the Singapore endpoint** — keep all calls there. Some models (notably `qwen-long`) are **Beijing-only** and won't be covered.

---

## 2. LLMs — model IDs & context windows

| Model ID | Context (max input) | Max output | Best for | Conf. |
|---|---|---|---|---|
| **`qwen3.7-max`** (snapshots `…-2026-05-20`, `…-2026-06-08`) | **1,000,000** | ~32–65K (unconfirmed) | Flagship: native reasoning + native iterative function-calling; OpenAI + Anthropic API compatible. **Our reasoning + final-answer model.** | high (ctx) `[web search]` |
| **`qwen-plus`** | up to **1,000,000** (default usable ~129,024 unless `max_input_tokens` raised) | 32,768 | Balanced cost/perf. **Our routine-extraction default.** | med `[web search]` |
| **`qwen-flash`** | up to **1,000,000** | — | Cheapest; supports **context caching** (amortise the stable brief prefix). | med `[web search]` |
| `qwen-turbo` | up to **1,000,000** | 16,384 | Fast/cheap. | med |
| `qwen3-max` / `qwen-max` | **~262,144 (256K)** | 32,768 | Strong reasoning/coding. | med `[web search]` |
| `qwen-long` | **10,000,000** (via file-id upload) | 32,768 | Bulk doc ingestion. **Beijing-only — avoid for us.** | med `[verified region]` |
| `qwen3-coder-plus` | 1,000,000 | 65,536 | Coding/agentic. | med |

**Gotcha:** 1M-context models default to ~129K usable input. Opt into the big window with `max_input_tokens` only if you actually need it — Trace deliberately keeps context small.

---

## 3. Embeddings & rerank (the retrieval pipeline)

| Model | Dimensions | Max input | Languages | Price | Conf. |
|---|---|---|---|---|---|
| **`text-embedding-v4`** (Qwen3-Embedding) | Matryoshka: 2048 / 1536 / **1024 (default)** / 768 / 512 / 256 / 128 / 64 | 8,192 tok | 100+ | ~$0.07/1M | high `[verified]` |
| `text-embedding-v3` | 1024 / 768 / 512 | 8,192 | 50+ | 500K free tok (SG) | high `[verified]` |

- **Use `text-embedding-v4` @ 1024-dim** — the cost/quality sweet spot; go 1536/2048 only if precision demands. Params: `text_type` ("query" vs "document" — matters for asymmetric retrieval), `dimension`, `output_type` ("dense"/"sparse"/"dense&sparse").
- **Rerankers** (apply *after* vector recall): `qwen3-rerank` (100+ langs) or `gte-rerank-v2` (recommended, 50+ langs). Hosted limits `[verified — doc]`: **≤ 500 docs, 4,000 tokens/item**, qwen3-rerank ≤120,000 tok/request (SG), gte-rerank-v2 ≤30,000 (Beijing). *(The "32K context" you'll see online is the open-source Qwen3-Reranker model, NOT the hosted API limit.)* Note: legacy `gte-rerank` (v1) is **discontinued 30 May 2026** — use `gte-rerank-v2`.

**Pipeline:** `text-embedding-v4 (1024d)` → vector store → `qwen3-rerank` → composite re-score (relevance+recency+importance, filter `valid_to IS NULL`) → retrieve-to-budget top-k.

---

## 4. Function calling / tool use `[high]`

- Supported across current Qwen3.x models via the standard OpenAI **`tools`** parameter on the compatible endpoint (`{"type":"function","function":{name,description,parameters}}`); `tool_call_id` links results to calls (OpenAI semantics).
- `qwen3.7-max` explicitly supports **native function-calling + iterative multi-step tool invocation** (and Anthropic tool-use protocol in preview).

---

## 5. MCP & "custom skills" — the judging hook

Judging rewards "custom skills, MCP integrations." Options, most-to-least directly usable:

1. **Qwen-Agent** (`github.com/QwenLM/Qwen-Agent`, Qwen ≥ 3.0) — **our pick.** Ships Function Calling, **MCP client** (install extra `[mcp]`, tools via an MCP config file), Code Interpreter, RAG, a memory module, and **custom tools** via the `@register_tool` decorator + `BaseTool`. Backends: DashScope or any OpenAI-compatible server. `[web search]`
2. **Model Studio MCP Marketplace** — platform-hosted MCP servers; Alibaba exposes 60+ cloud products via an MCP-compatible "Skill" platform.
3. **AgentScope** + AgentScope Platform (live ~11 Jun 2026: Skill marketplace, MCP tool whitelisting) — if we ever want multi-agent.
4. Spring AI Alibaba — JVM only.

**Plan:** expose `capture_decision`, `check_invalidation`, `recall_decisions`, `supersede_decision` as Qwen-Agent **MCP tools / custom skills** — this is the most direct way to bank the hook, and it's demonstrable on camera (the agent visibly calls tools).

---

## 6. Credits / quota `[web search]`

- **$40 coupon per participant** (request via the hackathon coupon form).
- **Model Studio new-user free quota:** ~**1,000,000 free tokens per model** across ~70 Qwen models, ~**90 days**, **Singapore only**, **real-time inference only** (excludes batch, context caching, fine-tuning, deployment). `text-embedding-v3` has its own 500K free quota.
- **Unverified:** whether the $40 coupon covers embeddings/rerank/context-caching, and qwen3.7-max's SG availability/price (unannounced at launch). **Mitigation:** default to qwen-plus/flash; reserve qwen3.7-max for the hard contradiction reasoning.

---

## 7. Minimal call sketch (OpenAI-compatible, Python) `[inference — illustrative, verify model availability]`

```python
from openai import OpenAI
client = OpenAI(
    api_key="<DASHSCOPE_KEY>",
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",  # Singapore
)

# reasoning / extraction with function calling
resp = client.chat.completions.create(
    model="qwen3.7-max",                 # or qwen-plus for routine extraction
    messages=[{"role": "system", "content": SYSTEM_PROMPT},
              {"role": "user", "content": transcript_chunk}],
    tools=[CAPTURE_DECISION_TOOL, CHECK_INVALIDATION_TOOL],
    # max_input_tokens=1_000_000,        # only if you truly need the big window
)

# embeddings
emb = client.embeddings.create(
    model="text-embedding-v4",
    input=[decision.statement + " " + decision.rationale],
    dimensions=1024,
)
```

---

*Sources: alibabacloud.com Model Studio docs (endpoints, embeddings, qwen-long, rerank, free-quota); marktechpost / datastudios / juheapi (model context windows); github.com/QwenLM/Qwen-Agent. Full list in [.research/research-qwen-tech.md](../.research/research-qwen-tech.md) and verification in [.research/verification.md](../.research/verification.md).*
