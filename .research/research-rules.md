## SUMMARY
The event is the "Global AI Hackathon Series with Qwen Cloud," sponsored by Alibaba Cloud / Qwen Cloud and managed by Devpost (qwencloud-hackathon.devpost.com). It is a 100% online global hackathon with five competition tracks (called "arenas"): Track 1 MemoryAgent, Track 2 AI Showrunner, Track 3 Agent Society, Track 4 Autopilot Agent, and Track 5 EdgeAgent. Total prize pool is "$70,000+" in cash and Alibaba Cloud credits. The user is correct that the multi-agent track ("Agent Society") is Track 3, and the user's data point of "Technical Depth & Engineering (30%)" is confirmed as one of four judging criteria weighted 30/30/25/15.

Key dates: launched ~May 26, 2026; build period through early July; the official submission deadline is July 9, 2026 at 2:00 PM PDT (which equals July 10, 2026 02:30 IST — this reconciles the Internshala listing). Alibaba Cloud's own tweet rounds this to "Submit by July 8, 2026." Judging runs roughly July 10-30 with winners announced around August 7, 2026. So yes, the hackathon concludes in July (judging spills into late July/early August). The user's "in July" is confirmed.

Per-track prize is $10,000 ($7,000 cash + $3,000 Alibaba Cloud credits) for the winner of each of the 5 tracks, plus 10 "Blog Post" awards and 10 "Honorable Mentions" each worth ~$1,000 ($500 cash + $500 credits), plus swag, Qwen Cloud blog feature, AI Catalyst Program eligibility and Qwen Ambassador opportunity. Teams are 1-5 members; entrants must be of legal age of majority; submissions must be original work and must use Qwen models available on Qwen Cloud. Teams retain IP ownership but grant the Sponsor a non-exclusive license for judging and promotion.

IMPORTANT confidence caveats: (1) the two 30% criteria descriptions were reported with their text swapped between two sources, so the label-to-description mapping for those two is uncertain (labels + weights are solid). (2) Demo video length is reported as "under 3 minutes" by the Devpost rules snippet but "max 5 minutes" by one mirror — treat 3 minutes as most likely but verify. (3) I could not load the official Devpost page directly (it renders empty / is JS-heavy), so all exact wording comes from search snippets and secondary mirrors, not from my own read of the primary rules page.

## KEY FINDINGS
- **[high]** Official name is 'Global AI Hackathon Series with Qwen Cloud', sponsored by Alibaba Cloud / Qwen Cloud and managed by Devpost; it is 100% online and global.
  - evidence: Devpost title: 'Global AI Hackathon Series with Qwen Cloud : Build your own AI Agent on Qwen Cloud - compete for $70K in prizes across five tracks.' Sponsor = Alibaba Cloud, infrastructure = Qwen Cloud LLM platform, managed by Devpost.
  - source: https://qwencloud-hackathon.devpost.com/ ; https://internshala.com/competitions/global-ai-hackathon-series-with-qwencloud/
- **[high]** There are exactly five tracks in this order: 1 MemoryAgent, 2 AI Showrunner, 3 Agent Society, 4 Autopilot Agent, 5 EdgeAgent.
  - evidence: Alibaba Cloud tweet: '...5 tracks: MemoryAgent, AI Showrunner, Agent Society, Autopilot Agent, and EdgeAgent.' Confirmed by qwencloud.com and Internshala which number them 1-5 in this order.
  - source: https://x.com/alibaba_cloud/status/2062380528452448437
- **[high]** Track 1 MemoryAgent: build an agent with persistent memory that accumulates experience, remembers user preferences, and makes increasingly accurate decisions across multi-turn, cross-session interactions; focus on efficient memory storage/retrieval, timely forgetting, and recalling critical memories within limited context windows.
  - evidence: 'Build an Agent with persistent memory that autonomously accumulates experience, remembers user preferences, and makes increasingly accurate decisions across multi-turn, cross-session interactions.' Plus focus on 'efficient memory storage and retrieval, timely forgetting of outdated information, and recalling critical memories within limited context windows.'
  - source: https://www.qwencloud.com/challenge/hackathon
- **[high]** The multi-agent track is Track 3 'Agent Society' (user's guess confirmed): design a multi-agent collaboration system where agents with distinct capabilities divide tasks, dialogue, and negotiate, showing measurable efficiency gains over a single-agent baseline.
  - evidence: 'Design a cooperative multi-agent cluster where distinct AI personas partition tasks, resolve logic conflicts and negotiate solutions while demonstrating efficiency gains versus single-agent approaches.' Examples: negotiation marketplaces, debate platforms with a judge, cooperative problem-solving swarms.
  - source: https://internshala.com/competitions/global-ai-hackathon-series-with-qwencloud/ ; https://qwencloud-hackathon.devpost.com/
- **[high]** Four judging criteria summing to 100%: Technical Depth & Engineering 30%, Innovation & AI Creativity 30%, Problem Value & Impact 25%, Presentation & Documentation 15%.
  - evidence: All four labels and weights confirmed by qwencloud.com fetch and Devpost search snippet; user's 'Technical Depth & Engineering (30%)' matches. 30+30+25+15 = 100.
  - source: https://www.qwencloud.com/challenge/hackathon ; https://qwencloud-hackathon.devpost.com/
- **[medium]** The detailed descriptions for the two 30% criteria were reported swapped between sources, so which 30% bucket owns 'sophisticated API/MCP use' vs 'architecture/code quality' is uncertain.
  - evidence: qwencloud.com maps 'sophisticated use of Qwen Cloud APIs, custom skills, MCP integrations' to Innovation & AI Creativity; the Devpost snippet maps that same text to Technical Depth & Engineering. Labels and weights agree; description-to-label mapping does not.
  - source: https://www.qwencloud.com/challenge/hackathon ; https://qwencloud-hackathon.devpost.com/
- **[high]** Submission deliverables (on Devpost): public GitHub repo, demo video, presentation deck/PPT, written project description, and an architecture diagram. Demo video must be public on YouTube/Vimeo/Youku.
  - evidence: 'Final deliverables must be uploaded to Devpost, including repository, demo video, deck, and project description... include an Architecture Diagram.' Video 'uploaded to and made publicly visible on YouTube, Vimeo, or Youku, with a link provided on the submission form.'
  - source: https://qwencloud-hackathon.devpost.com/rules ; https://www.qwencloud.com/challenge/hackathon
- **[medium]** Demo video length limit is most likely under 3 minutes, though one mirror says max 5 minutes.
  - evidence: Devpost rules snippet: 'The demo video should be less than three (3) minutes.' qwencloud.com fetch: 'Demo video (maximum 5 minutes).' Sources conflict.
  - source: https://qwencloud-hackathon.devpost.com/rules ; https://www.qwencloud.com/challenge/hackathon
- **[medium]** Official submission deadline is July 9, 2026 at 2:00 PM PDT (= July 10, 2026 02:30 IST). Alibaba Cloud's tweet rounds it to 'Submit by July 8, 2026.'
  - evidence: Devpost snippet: 'deadline is July 9, 2026 @ 2:00pm PDT.' Internshala shows 'July 10, 2026 @ 2:30 AM GMT+5:30' (the same instant). Tweet: 'Submit by July 8, 2026.'
  - source: https://qwencloud-hackathon.devpost.com/rules ; https://internshala.com/competitions/global-ai-hackathon-series-with-qwencloud/ ; https://x.com/alibaba_cloud/status/2062380528452448437
- **[medium]** Timeline: launch ~May 26, 2026; build period May 26 - early July; judging ~July 10-30, 2026; winners announced ~August 7, 2026.
  - evidence: qwencloud.com fetch: 'May 26, 2026 Official Launch; May 26-July 8 Build; July 9 Submission Deadline; July 10-30 Judging; August 7 Winners Announced.'
  - source: https://www.qwencloud.com/challenge/hackathon
- **[high]** Total prize pool is '$70,000+'; each of the 5 track winners gets $10,000 ($7,000 cash + $3,000 Alibaba Cloud credits).
  - evidence: Devpost tagline 'compete for $70K in prizes across five tracks'; 'Each track offers $7,000 cash + $3,000 cloud credits.' User's $7,000/track data point confirmed (it is the cash portion).
  - source: https://qwencloud-hackathon.devpost.com/ ; https://www.qwencloud.com/challenge/hackathon
- **[medium]** Additional awards: 10 Blog Post winners and 10 Honorable Mentions, each ~$1,000 ($500 cash + $500 credits); plus swag, Qwen Cloud blog feature, AI Catalyst Program eligibility, and Qwen Ambassador opportunity.
  - evidence: '10 Blog Post winners: $500 cash + $500 credits each; 10 Honorable Mentions: $500 cash + $500 credits each.' Winners get 'AI Catalyst Program eligibility + Ambassador opportunity' and blog feature.
  - source: https://internshala.com/competitions/global-ai-hackathon-series-with-qwencloud/ ; https://www.qwencloud.com/challenge/hackathon
- **[high]** Eligibility: open globally (except restricted countries), must be of legal age of majority; teams of 1-5 members; solo entrants may form teams.
  - evidence: 'Teams of 1-5 members are allowed'; 'above legal age of majority in their respective country or territory'; 'Open globally except restricted nations.'
  - source: https://internshala.com/competitions/global-ai-hackathon-series-with-qwencloud/ ; https://www.qwencloud.com/challenge/hackathon
- **[high]** IP/originality: submission must be the entrant's original work and solely owned (open-source components allowed); direct copying of open-source projects is prohibited; teams retain IP but grant Sponsor a non-exclusive license for judging and promotion.
  - evidence: 'Your submission must (a) be your original work product; (b) solely owned by you... except for components licensed under applicable open source licenses.' 'Sponsor will have a non-exclusive license to use such entry for judging... and promoting.' 'Direct copying of open-source projects is prohibited.'
  - source: https://qwencloud-hackathon.devpost.com/rules
- **[medium]** Qualifying projects must use Qwen models available on Qwen Cloud (Qwen Cloud API); participants receive cloud coupons (~$40) to build.
  - evidence: 'Entrants must build a project using Qwen models available on Qwen Cloud.' 'Projects must use Qwen Cloud API'; '$40 worth of coupon provided per participant.'
  - source: https://qwencloud-hackathon.devpost.com/rules ; https://www.qwencloud.com/challenge/hackathon

## STRUCTURED
## Global AI Hackathon Series with Qwen Cloud — Research Findings

### 1. Identity / Organizer / "Series"
- **Official name:** Global AI Hackathon Series with Qwen Cloud (also styled "Qwen Cloud Global AI Hackathon Series"). [high]
- **Sponsor:** Alibaba Cloud / Qwen Cloud (built on Alibaba's frontier Qwen models). **Managed/hosted by:** Devpost at `qwencloud-hackathon.devpost.com`. [high]
- **Format:** Described as "100% Online" and global. Five tracks are branded as "arenas" ("Choose your arena!"). [high]
- **"Series" note:** I found no clear evidence of separate regional/offline events tied to THIS Devpost hackathon — the "Series" branding most plausibly refers to it being the first of a recurring program and/or the multi-arena (5-track) structure. There is a *separate* in-person Alibaba/Qwen event ("Qwen AI Build Day," pitched live in Ho Chi Minh City) that is NOT the same Devpost competition. Treat any "regional offline events" claim as unconfirmed. [low confidence on the offline/regional question]

### 2. The Five Tracks — exact/near-exact wording
> Note: Track descriptions below are from secondary mirrors (Internshala, qwencloud.com, Devpost search snippets). The official Devpost page renders empty to automated fetch, so these are quoted from snippets, not from a direct read of the primary rules text. Wording is very close to official but should be verified verbatim on the live page.

**Track 1 — MemoryAgent** [high]
"Build an Agent with persistent memory that autonomously accumulates experience, remembers user preferences, and makes increasingly accurate decisions across multi-turn, cross-session interactions."
Focus areas: efficient memory storage and retrieval; timely forgetting of outdated information; recalling critical memories within limited context windows (vector storage, forgetting mechanisms, context optimization).

**Track 2 — AI Showrunner** [high]
"Leverage video generation capabilities (such as Wan / HappyHorse) to build an Agent that autonomously handles the entire short drama creation pipeline — from scriptwriting and storyboarding to video generation and editing." (Reported to have the highest token allowance of the tracks.)

**Track 3 — Agent Society (the multi-agent track — user's guess CONFIRMED as Track 3)** [high]
"Design a multi-agent collaboration system where multiple Agents with distinct capabilities work together through task division, dialogue, and negotiation to accomplish complex tasks." Participants should show how agents decompose tasks and assign roles, how they resolve disagreements/execution conflicts, and demonstrate a **measurable efficiency gain over single-agent baselines**. Example scenarios: a simulated marketplace where buyer/seller agents negotiate; a multi-agent debate platform with a judge; cooperative problem-solving swarms.

**Track 4 — Autopilot Agent** [high]
"Build an Agent that automates real-world business workflows end-to-end. Scenarios are open-ended — for example, from customer inquiry emails to quote generation, from system alerts to automated remediation, or from resume screening to interview scheduling. Participants should demonstrate the Agent's ability to handle ambiguous inputs, invoke external tools, and incorporate human-in-the-loop checkpoints at critical decision points. Emphasis is on production-readiness over toy demos."

**Track 5 — EdgeAgent** [high]
"Embed Qwen-powered intelligence into physical devices (robots, IoT agents, smart hardware) that perceive via edge sensors, reason via cloud APIs/Skills, and act locally," with graceful degradation during network interruptions.

### 3. Judging Criteria + Weights (sum = 100%)

| # | Criterion | Weight | Reported description |
|---|-----------|--------|----------------------|
| 1 | **Technical Depth & Engineering** | **30%** | Architecture quality, modularity, scalability, error handling, clean code/non-trivial logic, tech-stack sophistication (advanced patterns). *[See swap note.]* |
| 2 | **Innovation & AI Creativity** | **30%** | Sophisticated use of Qwen Cloud APIs (e.g., custom skills, MCP integrations); algorithmic/engineering innovation via novel solutions, custom components, performance optimization. *[See swap note.]* |
| 3 | **Problem Value & Impact** | **25%** | Real-world relevance (solves an authentic technical/business pain point); scalability potential for productization or open-source/community adoption. |
| 4 | **Presentation & Documentation** | **15%** | Clear technical demo with key logic visualized effectively; clear documentation. |

- Labels + weights are **high confidence** and consistent across sources; they match the user's "Technical Depth & Engineering (30%)" data point and sum to 100%.
- **SWAP CAVEAT [medium]:** Two sources disagreed on which of the two 30% buckets carries the "sophisticated Qwen API / MCP use" description vs the "architecture/code quality" description. qwencloud.com puts "API/MCP sophistication" under *Innovation & AI Creativity* and "architecture/code quality" under *Technical Depth & Engineering*; the Devpost snippet reversed them. Verify the exact pairing on the live rules page. The label↔weight pairing itself is not in doubt.

### 4. Submission Requirements / Deliverables (submitted on Devpost) [high unless noted]
- **Public source-code repository** (GitHub).
- **Demo video** — must be uploaded and publicly visible on YouTube, Vimeo, or Youku, with the link on the submission form. **Length: most likely under 3 minutes** (Devpost rules snippet: "less than three (3) minutes"); one mirror says "max 5 minutes" — *conflict, verify* [medium].
- **Presentation deck / PowerPoint.**
- **Written project description.**
- **Architecture diagram** (clear visual of the system).
- No mention of a mandatory synchronous **live pitch** for general entrants (judging is async over the judging window). [medium — absence of evidence]

### 5. Key Dates [medium]
- **Launch / registration open:** ~May 26, 2026.
- **Build period:** ~May 26 → early July 2026.
- **Submission deadline:** **July 9, 2026, 2:00 PM PDT** (== July 10, 2026 02:30 IST, which reconciles the Internshala listing). Alibaba Cloud's tweet rounds this to "Submit by July 8, 2026" (marketing). 
- **Judging period:** ~July 10–30, 2026.
- **Winners announced:** ~August 7, 2026.
- User's "in July" is CONFIRMED (build + deadline in July; results spill to early August).

### 6. Prizes (total pool "$70,000+") [high on totals, medium on minor lines]
- **Per-track winner (×5 tracks):** $10,000 total = **$7,000 cash + $3,000 Alibaba Cloud credits**, plus Qwen Cloud blog feature, swag bag, AI Catalyst Program eligibility, and Qwen Ambassador opportunity. (User's "$7,000/track" = the cash portion.)
- **Blog Post awards (×10):** ~$1,000 each = $500 cash + $500 credits.
- **Honorable Mentions (×10):** ~$1,000 each = $500 cash + $500 credits.
- **Other:** Devpost achievement badges; ~$40 Qwen Cloud coupon per participant for building.
- Note: 5×$10k = $50k; plus 10×$1k + 10×$1k = $20k → ~$70k, consistent with "$70,000+". [inference, consistent]

### 7. Eligibility [high]
- Open to global developers/builders, **except residents of restricted/embargoed countries** (full list in official rules).
- Must be at/above the **legal age of majority** in the entrant's country/territory.
- **Team size: 1–5 members.** Solo entrants may form/join teams. No stated student-vs-professional restriction (open to professionals and students alike).

### 8. IP / Open-Source / Prior-Work Rules [high]
- Submission must be the entrant's/team's **original work product** and **solely owned** by them (third-party/open-source components allowed only under their applicable OSS licenses).
- **Direct copying of open-source projects is prohibited**; OSS libraries/frameworks may be used as building blocks.
- **Teams retain IP ownership** of their submissions. By entering, they grant the **Sponsor a non-exclusive license** to (a) judge/evaluate/test the submission and (b) promote/publicize/document the hackathon and results.
- Whether the project must be brand-new (built during the hackathon) vs pre-existing: the "original work" clause implies new/substantially-new work, but I did not find an explicit "must be created during the hackathon window" sentence — **verify on the official rules page** [medium].

### 9. Required Qwen / Alibaba Cloud usage [medium]
- Projects **must use Qwen models available on Qwen Cloud** (Qwen Cloud API) to qualify. Sophisticated use of Qwen Cloud APIs (custom Skills, MCP integrations) is explicitly rewarded in scoring.
- Some mirror text also said projects must be "deployed on Alibaba Cloud infrastructure" — treat the deployment requirement as **medium confidence**; the firm requirement is using Qwen models on Qwen Cloud.
- No single specific Qwen model version is mandated in the sources found (track-appropriate models, e.g. Wan/HappyHorse video models referenced for the AI Showrunner track).

### Verification gaps / what to confirm directly on Devpost
1. Exact demo-video length (3 min vs 5 min).
2. The description↔label pairing for the two 30% judging criteria.
3. Whether an explicit "must be built during the hackathon" clause exists.
4. Whether Alibaba Cloud *deployment* (not just Qwen Cloud API use) is mandatory.
5. Exact verbatim track text (my quotes are from snippets/mirrors, not a direct primary-source read — the Devpost page is JS-rendered and returned empty to automated fetch).

## OPEN QUESTIONS
- Is the demo video limit under 3 minutes (Devpost rules snippet) or max 5 minutes (one mirror)? Sources conflict.
- For the two 30%-weighted criteria, which one's official description carries 'sophisticated Qwen API / MCP use' vs 'architecture & code quality'? Sources swapped them.
- Does an explicit rule require the project to be newly built during the hackathon window, or are pre-existing projects allowed if extended?
- Is deployment on Alibaba Cloud infrastructure mandatory, or is using Qwen models on Qwen Cloud (API) sufficient to qualify?
- Does the 'Series' include any regional or in-person/offline events, or is it purely the single online 5-track competition? (Separate 'Qwen AI Build Day' offline events exist but appear distinct.)
- Is there any synchronous live-pitch/finals round for shortlisted teams, or is judging fully asynchronous?
- Exact verbatim official track descriptions and the full restricted-countries eligibility list (could not be read directly from the JS-rendered Devpost page).

## SOURCES
- https://qwencloud-hackathon.devpost.com/
- https://qwencloud-hackathon.devpost.com/rules
- https://qwencloud-hackathon.devpost.com/resources
- https://www.qwencloud.com/challenge/hackathon
- https://internshala.com/competitions/global-ai-hackathon-series-with-qwencloud/
- https://www.startupgrantsindia.com/global-ai-hackathon-series-with-qwen-cloud
- https://www.competehub.dev/en/competitions/devpost29966
- https://x.com/alibaba_cloud/status/2062380528452448437
- https://dev.events/conferences/global-ai-hackathon-series-with-qwen-cloud-clwafmmq
- https://www.linkedin.com/posts/devpost_alibaba-cloud-global-is-launching-the-global-activity-7465075046563274753-Uocc