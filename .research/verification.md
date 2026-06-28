# VERIFICATION

- **CONFIRMED**: Four judging criteria with weights summing to 100: Technical Depth & Engineering 30%, Innovation & AI Creativity 30%, Problem Value & Impact 25%, Presentation & Documentation 15%.
  - source: qwencloud.com/challenge/hackathon (WebFetch, ran) lists all four labels+weights; Devpost rules text via WebSearch corroborates the same four labels and 30/30/25/15 weights. 30+30+25+15=100. [verified — I read both]
- **CONTRADICTED**: The 'sophisticated use of Qwen Cloud APIs (custom skills / MCP integrations)' description belongs to the Technical Depth & Engineering (30%) bucket (TECH researcher's claim, cited to startupgrantsindia).
  - corrected: Sources genuinely conflict on the description<->label mapping for the two 30% buckets. qwencloud.com places 'Sophisticated use of Qwen Cloud APIs' AND 'Algorithm/engineering innovation' under Innovation & AI Creativity (30%), and 'architecture quality / code cleanliness / tech-stack sophistication' under Technical Depth & Engineering (30%). The Devpost-derived snippet reverses this (API/MCP under Technical Depth; architecture/modularity under Innovation). Labels and weights are solid; the API/MCP-to-Technical-Depth pairing is NOT reliably established — treat as unresolved.
  - source: qwencloud.com/challenge/hackathon (WebFetch) vs Devpost rules snippet (WebSearch). Direct conflict. [verified — I read both]
- **CONFIRMED**: Submission deadline is July 9, 2026 at 2:00 PM PDT (the hackathon concludes 'in July' 2026).
  - source: qwencloud.com (Submission Deadline July 9, 2026); Internshala (July 10, 2026 @ 2:30 AM GMT+5:30, which is the identical instant: July 9 2pm PDT = July 9 21:00 UTC = July 10 02:30 IST); Devpost via WebSearch ('July 9, 2026 at 2:00pm PDT'). Alibaba Cloud's tweet 'Submit by July 8, 2026' is marketing rounding. [verified — cross-checked timezone math]
- **CONFIRMED**: Timeline: Launch May 26, 2026; Build May 26 - July 8; Submission July 9; Judging July 10-30; Winners announced August 7, 2026.
  - source: qwencloud.com/challenge/hackathon (WebFetch, ran). Note: only this one source gave the full judging/winners timeline; launch + deadline are multiply corroborated, but the Judging July 10-30 and Winners Aug 7 dates rest on a single source. [verified — I read it; single-source on tail dates]
- **CONFIRMED**: Code repository must be open-sourced (public + open source license file).
  - source: Devpost rules via WebSearch: 'the repository must be public and open source by including an open source license file.' Plus originality clause: submission must be 'original work product, solely owned... except for components licensed under applicable open source licenses.' [verified — read snippet of primary Devpost rules]
- **CONTRADICTED**: The project must be newly built during the hackathon.
  - corrected: Existing projects ARE allowed if significantly updated. Devpost rules: 'Projects must be either newly created by the Entrant or, if the Entrant's Project existed prior to the Hackathon Submission Period, must have been significantly updated after the start of the Hackathon Submission Period.' So strictly-new is NOT required.
  - source: Devpost rules via WebSearch (qwencloud-hackathon.devpost.com/rules). [verified — read snippet]
- **CONFIRMED**: Per-track prize is $10,000 = $7,000 cash + $3,000 Alibaba/Qwen Cloud credits, for each of 5 track winners; total prize pool '$70,000+'.
  - source: qwencloud.com (WebFetch: '$7,000 cash' + '$3,000 cloud voucher each' per track), Devpost tagline '$70K in prizes across five tracks', Internshala ($7,000 + $3,000 per track). [verified — read]
- **CONFIRMED**: Additional awards: 10 Blog Post winners ($500 cash + $500 credits each) and 10 Honorable Mentions ($500 cash + $500 credits each).
  - source: qwencloud.com/challenge/hackathon (WebFetch, ran). Single strong source; math reconciles to ~$70K total (5x$10k + 10x$1k + 10x$1k = $70k). [verified — I read it]
- **CONFIRMED**: Embedding models on DashScope/Model Studio: text-embedding-v4 (Qwen3-Embedding; Matryoshka dims 2048/1536/1024-default/768/512/256/128/64; 8,192-token input; 100+ languages) and text-embedding-v3 (1024/768/512 dims; 50+ languages).
  - source: alibabacloud.com/help/en/model-studio/embedding (WebFetch, primary vendor doc). Confirms exact dimension list, 8,192 input, 100+ languages, $0.07-0.072/1M pricing. [verified — read primary doc]
- **CONFIRMED**: Reranker models available: gte-rerank-v2 and qwen3-rerank.
  - corrected: Both names confirmed, with serving-spec clarifications: hosted qwen3-rerank (Singapore) = 100+ languages, max 500 docs, max 4,000 input tokens PER ITEM, 120,000 tokens per request (NOT a 32K serving context — the '32K' is the open-source Qwen3-Reranker model's context, not the DashScope hosted limit). gte-rerank-v2 (Beijing) = 50+ languages, 500 docs, 4,000 tokens/item, 30,000/request. The older gte-rerank is being discontinued May 30, 2026. A multimodal qwen3-vl-rerank also exists (Beijing).
  - source: alibabacloud.com/help/en/model-studio/text-rerank-api (WebFetch, primary doc) for hosted limits; HuggingFace/Qwen blog for open-source 32K context. [verified — read primary doc]
- **CONFIRMED**: qwen3.7-max: 2026 flagship with 1,000,000-token context, native function calling/iterative tool use, OpenAI- and Anthropic-API compatible.
  - source: marktechpost.com (1M context launch May 2026), plus corroborating ofox.ai, chatforest.com, byteiota.com, yottalabs.ai (Anthropic Messages-format drop-in, tool calling). Multiple independent secondary sources. [web search — not a primary vendor spec page, but strongly multiply-sourced]
- **CONFIRMED**: qwen-plus, qwen-turbo, qwen-flash each support up to 1,000,000-token context (default usable input ~129,024 unless max_input_tokens is raised); qwen-flash adds context caching.
  - source: datastudios.org and digitalapplied.com (WebSearch) both state qwen-plus/turbo/flash = 1M with ~129,024 default cap and qwen-flash context caching. [web search — two corroborating secondary sources]
- **CONFIRMED**: qwen3-max context window = 262,144 (256K) tokens.
  - corrected: Confirmed at ~256K. juheapi states '256,000-token context window'; marktechpost confirms the prior Max tier was 256K ('up from 256K on Qwen3.6 Max'). The exact integer 262,144 (=256x1024) is plausible but the secondary source rounds to 256,000; treat 256K as solid, the precise 262,144 figure as not independently pinned.
  - source: juheapi.com qwen3-max guide (256,000); marktechpost.com (256K prior Max tier). [web search]
- **CONFIRMED**: Largest available Qwen context window = qwen-long at 10,000,000 tokens (via file-id upload, not raw prompt), Beijing region only; max output 32,768.
  - source: alibabacloud.com/help/en/model-studio/long-context-qwen-long (WebFetch, primary doc): 10M total context, fileid://{FILE_ID} mechanism, 32,768 max output, Chinese mainland (Beijing) region only. Corroborated by datastudios.org/digitalapplied.com (10M is the ceiling of the Qwen range). [verified — read primary doc]
- **CONFIRMED**: Five tracks in order: 1 MemoryAgent, 2 AI Showrunner, 3 Agent Society (the multi-agent track), 4 Autopilot Agent, 5 EdgeAgent.
  - source: Alibaba Cloud X/tweet lists all five; qwencloud.com and Internshala number them. Track 3 = Agent Society (multi-agent) confirmed. [web search + read]
- **CONFIRMED**: Team size 1-5 members.
  - source: qwencloud.com (WebFetch: 'Teams of 1-5 members allowed'); Internshala ('solo or form teams'). [verified — read]

## NOTES
CONFIDENCE/METHOD: Devpost pages (qwencloud-hackathon.devpost.com/*) render EMPTY to WebFetch as warned — I confirmed this (one attempt returned no content). All Devpost-rules quotes therefore come from WebSearch snippets, NOT a direct read. qwencloud.com (the official Qwen Cloud challenge page) DID load via WebFetch and is my strongest primary-ish rules source. competehub.dev and startupgrantsindia.com both returned HTTP 403 to WebFetch (could not independently read them).

KEY THINGS THE RESEARCHERS GOT WRONG OR THAT NEED FLAGGING:
1. JUDGING-CRITERIA DESCRIPTION SWAP IS REAL AND UNRESOLVED. The TECH researcher asserted as a finding that 'Technical Depth & Engineering (30%) ... cites sophisticated use of QwenCloud APIs (custom skills, MCP integrations)'. The official qwencloud.com page directly CONTRADICTS this: it puts 'Sophisticated use of Qwen Cloud APIs' under Innovation & AI Creativity (30%), and architecture/code-quality under Technical Depth. Do NOT hard-rely on 'API/MCP = Technical Depth'. Labels + weights (30/30/25/15) are rock-solid; the description-to-label mapping for the two 30% buckets is genuinely conflicting across sources.

2. 'PROJECT MUST BE NEWLY BUILT' IS FALSE. Devpost rules explicitly allow pre-existing projects if 'significantly updated after the start of the Hackathon Submission Period.' Both researchers left this as an open question / implied new-only; the actual rule permits extended existing projects.

3. CODE OPEN-SOURCE REQUIREMENT IS STRONGER THAN STATED. It is not merely 'a public GitHub repo' — the Devpost rules require the repo be 'public and open source' WITH an open-source license file. Confirmed.

4. qwen3-rerank SERVING LIMITS != open-source model. The DashScope-hosted qwen3-rerank caps at 4,000 input tokens PER document item and 120,000 tokens per request (max 500 docs), Singapore region. The '32K context' figure the TECH researcher cited is the open-source Qwen3-Reranker model's context, not the hosted API limit. Also: a multimodal qwen3-vl-rerank exists (Beijing), and the legacy gte-rerank is being discontinued May 30, 2026 (gte-rerank-v2 remains, Beijing, 50+ langs).

5. DEMO VIDEO LENGTH STILL CONFLICTS. qwencloud.com says 'Maximum 5 minutes'; the Devpost-rules snippet the RULES researcher cited says 'less than three (3) minutes.' I could not resolve this (Devpost won't render for direct read). Treat as unresolved — verify on the live Devpost rules page before relying on either.

6. DEPLOYMENT REQUIREMENT: A WebSearch summary of the Devpost overview states 'Projects must use Qwen Cloud API and be deployed on Alibaba Cloud infrastructure.' This supports a deployment requirement (the researchers marked it medium/uncertain). I could not confirm the exact wording from a directly-read primary source, so treat the 'deployed on Alibaba Cloud infrastructure' clause as probable-but-unverified.

7. qwen3.7-max pricing data point surfaced (not in researchers' scope): ofox.ai cites ~$2.50/MTok. Web-search only, single source, not verified.

EVERYTHING ELSE CHECKS OUT: deadline (July 9 2026 2pm PDT, reconciles with Internshala's July 10 02:30 IST), full date timeline (tail dates single-sourced to qwencloud.com), $70K+ pool, $7k+$3k per track, 10+10 secondary awards, team size 1-5, five tracks/order, qwen3.7-max 1M, qwen-plus/turbo/flash 1M, qwen3-max ~256K, qwen-long 10M (Beijing-only, largest), text-embedding-v4/v3 specs, gte-rerank-v2 + qwen3-rerank availability.