## SUMMARY
For a MemoryAgent on Track 1 of the Qwen Cloud Global AI Hackathon, the stack centers on Alibaba Cloud Model Studio (Chinese name "Bailian"/百炼), accessed via the DashScope API surface. Model Studio exposes the full Qwen family through both a native DashScope SDK and an OpenAI-compatible endpoint, so existing OpenAI/Anthropic SDK code works with a base-URL + API-key + model-name swap. For our use case (an agent managing a limited context window), the standout models are qwen3.7-max (1M-token reasoning + agentic tool-use flagship, released May 2026), the qwen-plus/turbo/flash tier (up to 1M context each), and qwen-long (a 10M-token document model that ingests files by file-id). qwen3-max sits at 256K (262,144) context. All current Qwen3.x models support native function calling/tool use via the standard OpenAI tools parameter; qwen3.7-max additionally advertises Anthropic-API compatibility (preview).

For memory retrieval, DashScope provides text-embedding-v4 (Qwen3-Embedding, Matryoshka dimensions from 64 up to 2048, 8,192-token input, 100+ languages, dense/sparse/hybrid output) and the older text-embedding-v3 (1024/768/512 dims). Reranking is available via gte-rerank-v2 and the newer qwen3-rerank (Qwen3-Reranker, 100+ languages, 32K context) — directly relevant to a retrieve-then-rerank memory pipeline. Caveat: I could not confirm the exact serving dimension count or top-N limits of qwen3-rerank from a primary doc; treat those as low-confidence.

On the "custom skills / MCP integrations" judging hook: MCP is first-class. The open-source Qwen-Agent framework (QwenLM/Qwen-Agent, built for Qwen>=3.0) ships function calling, MCP client support (install extra [mcp]), code interpreter, RAG, a memory/long-doc module, and @register_tool custom tools — it is the most direct framework to align our agent with. Model Studio also runs an MCP Marketplace, and Alibaba exposes 60+ cloud products via an MCP-compatible "Skill" platform. AgentScope (and its June-2026 Platform with a Skill marketplace + MCP tool whitelisting) and Spring AI Alibaba are the heavier multi-agent options. For credits, hackathon participants get a $40 coupon (requested via a form), stacking on Model Studio's standard new-user free quota of ~1M free tokens per Qwen model (Singapore region, ~90 days, real-time inference only).

Note: nearly all of this is from web search and vendor docs read via a summarizing fetch (not code I executed), so model IDs/numbers should be re-verified against the live Model Studio console before we hard-code them. A few figures conflict across sources (flagged inline).

## KEY FINDINGS
- **[high]** qwen3.7-max is the 2026 flagship: 1M-token context, native reasoning (chain-of-thought) plus native function calling / iterative tool use, and is OpenAI- and Anthropic-API compatible (Anthropic in preview).
  - evidence: 'features a 1M token context window'; 'supports function calling and iterative tool invocation natively'; 'compatible with both OpenAI and Anthropic API specifications' (Anthropic 'Preview'). Model ID qwen3.7-max (snapshots qwen3.7-max-2026-05-20, -2026-06-08). Up from 256K on Qwen3.6 Max.
  - source: https://www.marktechpost.com/2026/05/21/qwen-introduces-qwen3-7-max-a-reasoning-agent-model-with-a-1m-token-context-window/
- **[medium]** qwen-long offers a 10,000,000-token context window via a file-upload/file-id mechanism (not raw prompt) — ideal for bulk document ingestion, but Beijing-region only.
  - evidence: Model ID qwen-long-latest; 10M context; pass content as fileid://{FILE_ID} in a system message; output 32,768 tokens (one secondary source said 8,192); input $0.072/1M, output $0.287/1M; 'available only in the Chinese mainland (Beijing) region'.
  - source: https://www.alibabacloud.com/help/en/model-studio/long-context-qwen-long
- **[medium]** qwen-plus, qwen-turbo and qwen-flash each support up to ~1,000,000-token context, but default usable input is capped (~129,024) unless max_input_tokens is raised explicitly.
  - evidence: 'Qwen-Plus and Qwen-Turbo support up to 1,000,000 tokens, though by default usable input may be set to ~129,024 unless explicitly changed via max_input_tokens'; qwen-plus output 32,768, qwen-turbo output 16,384; qwen-flash adds context caching.
  - source: https://www.datastudios.org/post/qwen-context-window-token-limits-memory-policy-and-2025-rules
- **[medium]** qwen3-max (current non-3.7 max) has a 262,144-token (256K) context window and 32,768-token max output.
  - evidence: 'Qwen3-Max has a 262,144 token context window, with a maximum output of 32,768 tokens.' Older qwen-max snapshots were 32,768 input.
  - source: https://www.juheapi.com/blog/qwen3-max-context-window-guide-for-llm-models-256000-tokens
- **[high]** Model Studio's canonical access is OpenAI-compatible: swap key + base_url + model name. Singapore (international) OpenAI-compatible base URL is https://dashscope-intl.aliyuncs.com/compatible-mode/v1.
  - evidence: Docs: 'Model Studio provides an OpenAI-compatible interface'; legacy intl base_url https://dashscope-intl.aliyuncs.com/compatible-mode/v1; new recommended workspace endpoint https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1; China base is https://dashscope.aliyuncs.com/compatible-mode/v1.
  - source: https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope
- **[high]** text-embedding-v4 (Qwen3-Embedding) is the current embedding model: Matryoshka dims 64-2048 (default 1024), 8,192-token input, 100+ languages, batch 10, dense/sparse/hybrid output, ~$0.07/1M tokens.
  - evidence: Dimensions 2048/1536/1024(default)/768/512/256/128/64; max input 8,192; '100+ major languages'; output dense, sparse, or dense&sparse; $0.07/1M (Singapore). text-embedding-v3 = 1024/768/512 dims, 50+ languages, batch 50.
  - source: https://www.alibabacloud.com/help/en/model-studio/embedding
- **[medium]** Reranking is available for memory retrieval: gte-rerank-v2 (DashScope TextReRank, recommended) and the newer qwen3-rerank (Qwen3-Reranker, 100+ languages, 32K context).
  - evidence: 'DashScope Python SDK supports TextReRank with models like gte-rerank-v2'; supported-models page lists qwen3-rerank; 'Qwen3-Reranker ... supports 100+ languages, 32k context length' (open-source sizes 0.6B/4B/8B). Exact serving dims/top-N not confirmed from primary doc.
  - source: https://www.qwencloud.com/models/qwen3-rerank
- **[high]** Qwen-Agent (QwenLM/Qwen-Agent, for Qwen>=3.0) is the most directly aligned framework: function calling, MCP client support, code interpreter, RAG, memory, and custom tools via @register_tool / BaseTool.
  - evidence: 'Agent framework ... featuring Function Calling, MCP, Code Interpreter, RAG'; MCP via install extra [mcp] and an MCP config file; custom tools with @register_tool decorator; supports DashScope and OpenAI-compatible (vLLM/SGLang) backends; 'tool usage, planning, and memory'.
  - source: https://github.com/QwenLM/Qwen-Agent
- **[medium]** The hackathon's judging directly rewards the exact things we should lean on: 'Technical Depth & Engineering (30%)' explicitly cites sophisticated use of QwenCloud APIs such as custom skills and MCP integrations.
  - evidence: 'Technical Depth & Engineering (30%), which evaluates whether the project makes sophisticated use of QwenCloud APIs (e.g., custom skills, MCP integrations)'; other weights ~Innovation 30%, Problem Value/Impact 25%, Presentation/Docs 15%.
  - source: https://www.startupgrantsindia.com/global-ai-hackathon-series-with-qwen-cloud
- **[high]** Track 1 = MemoryAgent: persistent long-term memory, tracks user preferences, refines decisions across multi-turn cross-session interactions; judged on vector storage, forgetting of outdated info, and recalling critical memories within limited context windows.
  - evidence: 'long-term memory, tracks user preferences, and refines decisions across multi-turn, cross-session interactions' with focus on 'efficient memory storage and retrieval, timely forgetting of outdated information, and recalling critical memories within limited context windows'.
  - source: https://qwencloud-hackathon.devpost.com/
- **[medium]** Participants receive a $40 API coupon (via a coupon form), on top of Model Studio's standard new-user free quota of ~1M free tokens per Qwen model.
  - evidence: 'Participants will be provided $40 worth of coupon ... request free hackathon credits via a coupon form.' New-user quota: '1M free tokens per model across ~70 Qwen models ... valid for 90 days and only on the Singapore endpoint ... real-time inference only.'
  - source: https://www.alibabacloud.com/help/en/model-studio/new-free-quota
- **[medium]** MCP is first-class in the Alibaba ecosystem beyond Qwen-Agent: Model Studio runs an MCP Marketplace and exposes 60+ cloud products via an MCP-compatible Skill platform; AgentScope Platform (live June 2026) adds a Skill marketplace and MCP tool whitelisting.
  - evidence: 'Alibaba Cloud Ops MCP Server is officially available on the ... Model Studio Platform MCP Marketplace'; 'over 60 cloud products ... skills platform based on the Skill framework and compatible with the MCP format'; 'AgentScope Platform is live ... Skill marketplace ... MCP Tool Whitelisting' (v1.1.11, June 11 2026).
  - source: https://github.com/aliyun/alibaba-cloud-ops-mcp-server

## STRUCTURED
## 1. Qwen LLM family via API (2026) — model IDs, context windows

All accessible through Alibaba Cloud Model Studio / DashScope. Numbers below are from vendor docs + 2026 secondary sources read via summarizing fetch; verify against the live console before hard-coding. Where sources conflict it is flagged.

| Model ID | Context window (max input) | Max output | Notes / best for | Confidence |
|---|---|---|---|---|
| `qwen3.7-max` (snapshots `qwen3.7-max-2026-05-20`, `qwen3.7-max-2026-06-08`) | **1,000,000** | ~32K-65K (not explicitly confirmed) | 2026 flagship. Native reasoning (CoT) + native function calling / iterative tool use. OpenAI + Anthropic API compatible (Anthropic preview). Best all-round long-context + reasoning + agentic. | high (context); medium (output) |
| `qwen3.7-plus` | not confirmed (likely 256K-1M) | n/c | Multimodal w/ vision flagship (requires multimodal API). | low |
| `qwen3.6-plus` | 256K native, extendable toward 1M | n/c | Agentic coding model; reasoning on by default in Responses API. | medium |
| `qwen3.6-max-preview` | 256K | n/c | Prior max-tier preview. | medium |
| `qwen3.6-flash` / `qwen-flash` | up to **1,000,000** | n/c | Cheapest tier; supports **context caching** (useful for repeated memory prefixes). | medium |
| `qwen3-max` / `qwen-max` (current) | **262,144** (256K) | 32,768 | Strong reasoning/coding/math. (Older `qwen-max` snapshots were 32,768 input.) | medium |
| `qwen-plus` | up to **1,000,000** (default usable ~129,024 unless `max_input_tokens` raised) | 32,768 | Balanced cost/performance; reasoning variants exist. | medium |
| `qwen-turbo` | up to **1,000,000** (same default-cap caveat) | 16,384 | Fast/cheap. | medium |
| `qwen-long` (`qwen-long-latest`, `qwen-long-2025-01-25`) | **10,000,000** (via file-id, not raw prompt) | 32,768 (one source said 8,192) | Ultra-long document analysis; upload file -> `fileid://{FILE_ID}` in system msg. **Beijing region only.** Input $0.072/1M, output $0.287/1M. | medium |
| `qwen3-coder-plus` | **1,000,000** | 65,536 | Coding/agentic. | medium |
| Reasoning open variants e.g. `qwen3-235b-a22b-thinking-2507`, `qwen3-32b` | model-dependent | — | Explicit "thinking" models if a dedicated reasoner is wanted. | low |

**Largest context windows (relevant since our agent manages limited context):**
- `qwen-long` = 10M tokens (document/file ingestion path) — biggest, but Beijing-only.
- `qwen3.7-max`, `qwen-plus`, `qwen-turbo`, `qwen-flash`, `qwen3-coder-plus` = 1M tokens.
- `qwen3-max` = 256K.

**Best for long-context + reasoning:** `qwen3.7-max` (1M + native CoT + agentic tools) is the headline pick; `qwen-long` for bulk document recall; `qwen-plus`/`qwen-flash` for cheaper 1M-context working memory (use `qwen-flash` context caching to amortize a stable memory prefix).

> Caveat: 1M-context models default to a much smaller usable input (~129K) unless you set `max_input_tokens`. For a MemoryAgent this matters — you must opt into the big window.

## 2. API platform — Model Studio / Bailian / DashScope

- **Naming:** Model Studio (English) = Bailian / 百炼 (Chinese) = the platform. **DashScope** = the API/SDK surface. Get the API key from the Model Studio console.
- **Two call styles:** (a) native **DashScope SDK** (`pip install dashscope`, Python/Java) — fullest feature set; (b) **OpenAI-compatible** endpoint — reuse OpenAI SDK (Python/Node), just swap key + base_url + model name. There is also an OpenAI-compatible Responses API and Batch API.

| Region | OpenAI-compatible base URL | Native DashScope base URL |
|---|---|---|
| International (Singapore) — legacy | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | `https://dashscope-intl.aliyuncs.com/api/v1` |
| International (Singapore) — new recommended workspace endpoint | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...` |
| China (Beijing) | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/api/v1` |

- **Singapore vs China:** The free trial quota and most hackathon usage are on the **Singapore (international)** endpoint. Some models (notably `qwen-long`) are **Beijing-only**. Alibaba recommends migrating off `dashscope-intl.aliyuncs.com` to the per-workspace `…ap-southeast-1.maas.aliyuncs.com` domains for stability. `{WorkspaceId}` is on the Workspace Details page in the console.
- For Singapore, the workspace ID must be embedded in the base URL on the new endpoint.

Confidence: high for endpoints/SDK pattern (vendor docs); the exact new workspace-domain format is medium.

## 3. Embeddings & rerank (memory retrieval)

| Model | Dimensions | Max input tokens | Languages | Batch | Output types | Price | Confidence |
|---|---|---|---|---|---|---|---|
| `text-embedding-v4` (Qwen3-Embedding) | **2048, 1536, 1024 (default), 768, 512, 256, 128, 64** (Matryoshka) | 8,192 | 100+ | 10 | dense / sparse / dense&sparse | ~$0.07/1M (SG/HK), $0.072/1M (Beijing) | high |
| `text-embedding-v3` | 1024 (default), 768, 512 | 8,192 | 50+ | 50 | dense / sparse | free quota 500K tokens (SG) | high |

- Embedding call params: `text_type` ("query"/"document"), `dimension`, `output_type` ("dense"/"sparse"/"dense&sparse"). The query/document distinction matters for asymmetric memory retrieval.
- **Reranker (use after vector recall):**
  - `gte-rerank-v2` — recommended bilingual reranker, called via DashScope `TextReRank.call(model="gte-rerank-v2")`; predecessor `gte-rerank`.
  - `qwen3-rerank` (Qwen3-Reranker) — newer, listed on the supported-models overview; 100+ languages, ~32K context; open-source sizes 0.6B/4B/8B (Apache-2.0). Exact hosted top-N / doc limits **not confirmed** (low confidence).
- Recommended memory pipeline: `text-embedding-v4` (1024d is the cost/quality sweet spot; go 1536/2048 only for high precision) -> vector store -> `qwen3-rerank` / `gte-rerank-v2` rerank -> feed top-k into the agent's limited context.

## 4. Function calling / tool use

- Supported across current Qwen3.x models via the standard OpenAI **`tools`** parameter (`{"type":"function", "function":{name, description, parameters}}`) on the compatible-mode endpoint, and natively via DashScope. `tool_call_id` links results to calls (OpenAI semantics).
- `qwen3.7-max` explicitly supports **native function calling + iterative (multi-step) tool invocation**, plus Anthropic tool-use protocol (preview) — so Claude-tooling-style agents work.
- Docs: `model-studio/qwen-function-calling`; open Qwen docs `framework/function_call.html`.
- Confidence: high.

## 5. MCP & "custom skills" (the judging hook)

Judging rewards "custom skills, MCP integrations" under **Technical Depth & Engineering (30%)**. Options, most-to-least directly usable:

1. **Qwen-Agent** (`github.com/QwenLM/Qwen-Agent`, for Qwen>=3.0) — the closest fit. Ships: Function Calling, **MCP client** (install extra `[mcp]`, define tools via an MCP config file), Code Interpreter, **RAG**, a **memory / long-document** module, and **custom tools** via the `@register_tool` decorator + `BaseTool` interface. Backends: DashScope (with thinking-mode toggle) or any OpenAI-compatible server (vLLM/SGLang). Install extras: `[gui]`, `[rag]`, `[code_interpreter]`, `[mcp]`. This is the framework to align our MemoryAgent with for "custom skills + MCP" credit.
2. **Model Studio MCP Marketplace** — platform-hosted MCP servers (e.g., Alibaba Cloud Ops MCP Server). Alibaba also exposes **60+ cloud products** through an **MCP-compatible "Skill" platform**.
3. **AgentScope** (`agentscope-ai`) — flexible multi-agent framework. **AgentScope Platform went live ~June 11, 2026** with free QwenPaw deployment, a **plugin/Skill marketplace**, Free Model OAuth, and **MCP Tool Whitelisting** (v1.1.11). Good if we want multi-agent memory orchestration.
4. **Spring AI Alibaba** (`alibaba/spring-ai-alibaba`) — Java multi-agent framework with context-engineering best practices + an Admin platform with MCP management (only if we go JVM).

Confidence: high for Qwen-Agent capabilities; medium for marketplace/AgentScope platform specifics.

## 6. Free API credits / trial quota

- **Hackathon coupon:** participants get a **$40 API coupon**, requested via a coupon form (sign up for free trial -> request hackathon credits). Confidence: medium (search snippet, not a primary doc).
- **Standard Model Studio new-user quota:** ~**1,000,000 free tokens per Qwen model** across ~70 proprietary models (so tens of millions total), **valid 90 days** (first-time activations after 2025-09-08), **Singapore region only**, **real-time inference only** (excludes batch, context caching, fine-tuning, deployment). Doc: `model-studio/new-free-quota`. Confidence: medium-high.
- These stack, so practical budget for the hackathon is the $40 coupon + the per-model free quota. text-embedding-v3 additionally has its own 500K free-token quota (SG).

## 7. Official Qwen memory / agent frameworks to leverage or align with

- **Qwen-Agent** — function calling, MCP, RAG, memory, code interpreter, custom tools. Primary recommendation for Track 1. (high)
- **AgentScope** + **AgentScope Platform** (QwenPaw personal-assistant, Skill marketplace, MCP whitelisting, live June 2026) — multi-agent + persistent-assistant angle. (medium)
- **Spring AI Alibaba** + **AgentRun** + **PAI** — broader enterprise agent stack (JVM/infra). (medium)
- **Mobile-Agent** (Alibaba) — mobile GUI agent; only relevant if device/GUI control is in scope (not Track 1's core). (low)
- DashScope's own `qwen-long` file-id retrieval and `qwen-flash` context caching are platform-native primitives a MemoryAgent can exploit for cheap long-term recall.

## Conflicts / things to re-verify before relying on them
- `qwen-long` max output: 32,768 (official page) vs 8,192 (secondary). 
- `qwen-max` input: 262,144 for `qwen3-max` vs 32,768 for older `qwen-max` snapshots — confirm which alias the console serves.
- `qwen3.7-max` exact max output tokens — not stated in sources.
- `qwen3-rerank` hosted dimensions / top-N limits — unconfirmed.
- Hackathon submission deadline varies by source (July 8 tweet / July 9 devpost / July 10 02:30 GMT+5:30 internshala) — treat as ~July 8-10, 2026. Prizes: ~$70K+ total; per-track winner ~$7,000 cash + $3,000 cloud credits.

## OPEN QUESTIONS
- Exact max-output-token limits for qwen3.7-max and confirmation of its model availability/pricing on the Singapore endpoint (pricing was unannounced at launch).
- Is qwen-long (10M context) reachable from the Singapore/international endpoint, or strictly Beijing? If Beijing-only, our SG-quota credits may not cover it.
- qwen3-rerank hosted specifics on DashScope: served dimensions, max documents per call, top-N, and price vs gte-rerank-v2.
- Does the $40 hackathon coupon apply to embeddings/rerank and context caching, or only chat inference? And does it stack cleanly with the per-model 1M free quota?
- Definitive submission deadline (sources give July 8 vs 9 vs 10, 2026) and whether Track 1 has track-specific required APIs.
- Whether Model Studio offers a managed/native long-term memory service (vs us building retrieval on text-embedding-v4 + a vector DB like DashVector/Milvus) — Qwen-Agent has a memory module but a managed memory store was not confirmed.

## SOURCES
- https://www.alibabacloud.com/help/en/model-studio/models
- https://www.alibabacloud.com/help/en/model-studio/text-generation
- https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope
- https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-dashscope
- https://www.alibabacloud.com/help/en/model-studio/first-api-call-to-qwen
- https://www.alibabacloud.com/help/en/model-studio/embedding
- https://www.alibabacloud.com/help/en/model-studio/long-context-qwen-long
- https://www.alibabacloud.com/help/en/model-studio/qwen-function-calling
- https://www.alibabacloud.com/help/en/model-studio/new-free-quota
- https://www.alibabacloud.com/help/en/model-studio/model-pricing
- https://www.marktechpost.com/2026/05/21/qwen-introduces-qwen3-7-max-a-reasoning-agent-model-with-a-1m-token-context-window/
- https://www.datastudios.org/post/qwen-context-window-token-limits-memory-policy-and-2025-rules
- https://www.juheapi.com/blog/qwen3-max-context-window-guide-for-llm-models-256000-tokens
- https://github.com/QwenLM/Qwen-Agent
- https://qwen.readthedocs.io/en/latest/framework/qwen_agent.html
- https://qwen.readthedocs.io/en/latest/framework/function_call.html
- https://www.qwencloud.com/models/qwen3-rerank
- https://k-farruh.medium.com/mastering-text-embedding-and-reranker-with-qwen3-3284e7ae14c7
- https://qwencloud-hackathon.devpost.com/
- https://www.qwencloud.com/challenge/hackathon
- https://internshala.com/competitions/global-ai-hackathon-series-with-qwencloud/
- https://www.startupgrantsindia.com/global-ai-hackathon-series-with-qwen-cloud
- https://github.com/aliyun/alibaba-cloud-ops-mcp-server
- https://github.com/agentscope-ai/QwenPaw
- https://therouter.ai/news/qwen3-6-dashscope-api-routing/
- https://www.mindstudio.ai/blog/what-is-qwen-3-6-plus-agentic-coding-model