# 13 · UX & Demo Research — verified findings + action plan

*Deep research run 2026-07-03: 5 search angles → 23 sources → claim extraction → 3-vote adversarial verification per claim → synthesis. Every claim below survived 3-0 unless marked otherwise; two claims were refuted in verification and are listed so nobody re-believes them. Commissioned to answer: (1) minimalist/fluid ambient-assistant UI patterns, (2) what wins async Devpost judging, (3) fastest reliable desktop-demo tech for the video.*

## The action plan (synthesis of 23 confirmed claims)


- **P0-1 ** (~1h) Compliance audit of Qwen Track 1 checklist — public repo with real README, live testing link, <3-min publicly hosted video, text description, built-with tags [DQ evidence]. 
- **P0-2 ** (~3-4h) LLM formatting contract + chips: system prompt enforcing <=100 words prose / 1-2 sentences per paragraph / bullets for enumerables / answer-first order / accuracy caveats only [Intercom + NN/g], 2-3 suggested follow-up chips per answer plus a first-run empty state with capability explainer and 3-4 starter chips [NN/g truncated pyramid + Microsoft first-run], citation chips with direct quoted snippets from decision sources [Microsoft]. 
- **P0-3 ** (~4-6h) Video: elevator pitch in first ~15s, real screencast of the bubble over Revit/PDF, narrative arc, <3 min, doubles as live-link usage instructions; overflow detail to Devpost description [Devpost + judges]. 
- **P1-1 ** (~1-2h) Motion pass in vanilla CSS: open 250-300ms cubic-bezier(0.05,0.7,0.1,1); close 150-200ms cubic-bezier(0.3,0,0.8,0.15); micro-interactions 50-200ms [M3]. 
- **P1-2 ** (~30min) Filming shell: edge --app=URL + Win+Ctrl+T pin with PowerToys border disabled — confirmed primary path. 
- **P2** (timebox 2h, optional) pywebview frameless/on-top shell as fallback — viable since the transparency-is-broken claim was refuted, but do a 30-min spike first. Confirmed correct to keep Revit integration roadmap-only [thin-repo red flag + 'make sure it's a demo'].

## Verified findings

### Material Design 3 gives a directly copy-pastable motion contract for the Trace bubble

**Confidence:** high · **vote:** 3-0 on each of 4 merged claims

Material Design 3 gives a directly copy-pastable motion contract for the Trace bubble: a fixed duration-token scale (50-1000ms) where small-area transitions like a ~330px widget belong at the short-to-medium end (~150-300ms); emphasized-decelerate cubic-bezier(0.05, 0.7, 0.1, 1) for elements entering (card open) and emphasized-accelerate cubic-bezier(0.3, 0, 0.8, 0.15) for elements exiting (card close); and asymmetric timing — exits/dismissals should be shorter than entrances because they demand less attention. Concrete implementation: open the chat card in ~250-300ms with the decelerate curve, close it in ~150-200ms with the accelerate curve, keep in-card micro-interactions at 50-200ms.

> Verbatim from Google's first-party Motion.md (m3.material.io was 403-blocked): duration tokens motionDurationShort1-4 = 50/100/150/200ms, Medium1-4 = 250/300/350/400ms, Long1-4 = 450/500/550/600ms, ExtraLong1-4 = 700/800/900/1000ms; 'emphasized-decelerate... cubic-bezier: 0.05, 0.7, 0.1, 1 — easing used for animations that enter the screen'; 'emphasized-accelerate... cubic-bezier: 0.3, 0, 0.8, 0.15 — animations that exit the screen'; 'Transitions that exit, dismiss, or collapse an element use shorter durations. Exit transitions are faster because they require less attention than the user's nex

Sources: https://m3.material.io/styles/motion/easing-and-duration · https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md

### NN/g's April 2026 usability study of site AI chatbots directly validates Trace's short-sca

**Confidence:** high · **vote:** 3-0 on each of 3 merged claims

NN/g's April 2026 usability study of site AI chatbots directly validates Trace's short-scannable-answer plan: users treated chatbots like search bars (minimal typing, fast scannable answers, not conversation); long answers were tolerated only when formatted as bulleted lists rather than paragraphs; and NN/g's prescribed 'truncated-pyramid' rule says the first answer should contain only what was asked plus accuracy-critical caveats, with all extra detail progressively revealed via suggested follow-up prompts — i.e., generate 2-3 follow-up chips per answer, not longer answers. Formatting alone cannot rescue an over-long answer, and information order matters (answer first).

> Snippet-verbatim quotes (direct fetch 403-blocked): 'Participants often approached site chatbots much like search bars: they typed as little as possible, expected quick responses, and preferred answers they could scan quickly'; 'good writing for site AI chatbots should follow the truncated-pyramid rule, where extra detail is progressively revealed through suggested followup prompts. The first answer should include only what the user asked for and any caveats needed to keep that answer accurate'; Williams Sonoma example — participants appreciated 'bulleted lists instead of large paragraphs,' bu

Sources: https://www.nngroup.com/articles/less-chat-more-answer/

### Intercom's production Fin AI agent proves answer length should be an explicit, numeric LLM

**Confidence:** high · **vote:** 3-0 on each of 2 merged claims

Intercom's production Fin AI agent proves answer length should be an explicit, numeric LLM output contract, and provides copy-able numbers for Trace's ~330px card: official best-practice guidance caps answers at no more than 100 words with short sentences and at most 1-2 sentences per paragraph (the cap explicitly exempts code, bullet points, lists, and structured markdown), and the product ships exactly three tunable presets — Concise (~30% shorter), Standard (default), Thorough (~30% longer). Trace's system prompt should encode: <=100 words of prose, 1-2 sentences per paragraph, bullets for anything enumerable.

> Snippet-verbatim from Intercom's help docs (direct fetch 403-blocked; mirrored on fin.ai): 'Answers should be always readable and concise: sentences should be short, there should be at most 1-2 sentences per paragraph and no more than 100 words per answer (unless absolutely necessary)' — with the explicit exemption 'this guideline... does NOT apply to code, bullet points, lists, and other structured markdown.' Length presets: 'Concise being roughly 30% shorter than the Standard length... Thorough is roughly 30% longer'; Intercom reports Thorough yields only ~2% higher resolution rate than Conc

Sources: https://www.intercom.com/help/en/articles/10560969-fin-guidance-best-practices · https://www.intercom.com/help/en/articles/13177409-customize-fin-ai-agent-tone-of-voice-and-answer-length

### Microsoft's official generative-AI UX guidance validates three Trace design decisions simu

**Confidence:** high · **vote:** 3-0 on each of 3 merged claims

Microsoft's official generative-AI UX guidance validates three Trace design decisions simultaneously: (a) the floating-bubble pattern — an embedded single-entry point is 'ideal for tasks that require only occasional guidance' with 'context-aware assistance without occupying permanent screen space,' though explicitly not suited to complex/detailed interactions ('the more important the task, the more real estate required'); (b) suggested-prompt chips and an explanatory empty state — 'Microsoft studies show that users prefer an experience that explains what the copilot can do and gives them suggestions on how to begin'; (c) citation chips with quoted snippets — showing references makes the AI 'more likely to use responses from existing resources instead of fabricating' and prompts user verification, and 'integrating direct quotes from the source and directing the user to the specific location' supports fact-checking.

> All quotes verified verbatim against the canonical GitHub markdown source of the Microsoft Learn page (ms.date 09/16/2024; learn.microsoft.com itself 403-blocked). The first-run finding is independently corroborated by Microsoft's peer-reviewed HAX Guideline 1 ('Make clear what the system can do,' Amershi et al., CHI 2019). Design implication for Trace: keep the bubble for quick decision-recall Q&A, but note Microsoft's warning means deep tasks (e.g., browsing full decision history) may deserve an expand-to-larger-panel affordance; also carry Microsoft's own qualifier that 'showing references 

Sources: https://learn.microsoft.com/en-us/microsoft-cloud/dev/copilot/isv/ux-guidance · https://raw.githubusercontent.com/MicrosoftDocs/microsoft-cloud/main/docs/dev/copilot/isv/UX-Guidance.md

### Devpost's official guidance prescribes the exact video structure Trace planned

**Confidence:** high · **vote:** 3-0 on each of 4 merged claims

Devpost's official guidance prescribes the exact video structure Trace planned: open with the elevator pitch — what the app does and how it addresses the hackathon — in the first few seconds (because judges review many projects back-to-back), make the video an actual demo showing the project running (not slides or concept talk), keep it around/under three minutes (the norm for most hackathons; Qwen Track 1 mandates <3 min), and push overflow detail into the written Devpost text description rather than the video.

> Exact-phrase search-verified (direct fetch 403-blocked): 'Start the video with your elevator pitch. Explain what your app does and how it addresses the hackathon in the first few seconds of your video'; 'Make sure it's a demo — show your project or app in action... include more information in your text description if needed'; 'judges will likely review multiple projects back to back, so make sure to start your video with a quick overview'; 'Demo videos should showcase your project's features in around three minutes. Most hackathons have demo video requirements that are under three minutes long

Sources: https://info.devpost.com/blog/6-tips-for-making-a-hackathon-demo-video · https://help.devpost.com/article/84-video-making-best-practices · https://info.devpost.com/blog/understanding-hackathon-submission-and-judging-criteria

### Named Devpost judges describe how async judging is actually consumed

**Confidence:** high · **vote:** 3-0 on each of 2 merged claims

Named Devpost judges describe how async judging is actually consumed: storytelling in BOTH the video and the text description 'definitely helps keep the judges engaged and focused' (Karen Bajza-Terlouw, Databricks), and judges often attempt to use/test the live project first, falling back to the video for orientation when confused ('if you're confused about what to do... oftentimes the videos will help you' — Kelvin, Google). Implication: Trace's video needs a narrative arc (problem -> memory -> recall payoff) and must double as usage instructions for the live web link, and the Devpost description should tell the same story, not just list features.

> Quotes recovered via WebSearch snippets (direct fetch 403-blocked) from Devpost's own blog 'How to win a hackathon: Advice from 5 seasoned judges' — maximally relevant since the Qwen hackathon runs on Devpost. Qualifier from verification: the judges-test-the-project behavior comes from a games-track judge and is not universal — Devpost elsewhere states the video is 'often the first (and sometimes only!) thing that judges review' — so the video must stand alone AND the live link must be self-explanatory; the two-pronged advice covers both judge behaviors.

Sources: https://info.devpost.com/blog/hackathon-judging-tips

### Devpost online judging is fully asynchronous and self-serve — judges reach a dashboard onl

**Confidence:** high · **vote:** 3-0

Devpost online judging is fully asynchronous and self-serve — judges reach a dashboard only via an emailed 'Start Judging' link and step through submissions one at a time with no live pitch, Q&A, or team interaction — so every submission artifact (video, README, Devpost description, live link) must be independently self-explanatory with zero opportunity to clarify.

> Snippet-verbatim: 'The only way to get to your judging dashboard is to click Start Judging in the email you receive from Devpost.' Corroborated by Devpost docs showing judges work 'on their own schedule' stepping through submissions, and that live demos exist only in Devpost's separate offline-judging mode. Note: a companion claim that scoring is specifically 1-5 stars per criterion was REFUTED in verification (1-2 vote) — do not assume that scoring mechanism; assume only async, criteria-weighted review (Innovation 30%, Technical Depth 30%, Problem Value 25%, Presentation 15% per the Qwen brie

Sources: https://help.devpost.com/article/103-how-to-judge-an-online-hackathon · https://help.devpost.com/article/131 · https://help.devpost.com/article/101

### Two documented failure modes dictate Trace's priorities

**Confidence:** high · **vote:** 3-0 on each of 2 merged claims

Two documented failure modes dictate Trace's priorities: (1) 'many submissions are disqualified simply because they didn't meet the baseline criteria' — judges check stated requirements first, and missing required links, exceeding video length, or non-public assets are common DQs, so auditing the Qwen Track 1 checklist (public repo, live testing link, <3-min publicly hosted video, text description, built-with tags) outranks all polish; (2) polish masking thin substance backfires — judges explicitly dig into the GitHub repo, and 'the video intro looked really cool... but when you dug into the project or their GitHub, it was a lot lighter on code' is a named red flag, with 'ambiguity' and lack of code called out. Working substance plus a real README beats production value.

> Snippet-verified quotes from Devpost's blog and Help Center; independently corroborated by judge Bajza-Terlouw: 'surprising to see how many submissions did not fulfill the basic requirements.' Help Center confirms videos must be publicly hosted (YouTube/Vimeo) to embed for judges and that max video length is rule-enforced. This directly validates keeping Revit integration roadmap-only rather than faking it: a slick video over unimplemented claims is the exact red flag judges named.

Sources: https://info.devpost.com/blog/understanding-hackathon-submission-and-judging-criteria · https://info.devpost.com/blog/hackathon-judging-tips · https://help.devpost.com/article/126

### The primary filming plan is technically validated

**Confidence:** high · **vote:** 3-0 on each of 2 merged claims

The primary filming plan is technically validated: PowerToys Always On Top (default Win+Ctrl+T) is a system-wide Windows utility that pins the active window — including a chrome/edge --app=URL chromeless window, which is an ordinary top-level window — above all other windows, and it stays pinned when Revit/a PDF takes focus. One required correction: by default it draws a visible cyan border around the pinned window (DefaultFrameEnabled=true, #0099cc, 4px, 100% opacity per PowerToys source code), so for a clean floating-bubble shot you must toggle off 'Show a border around the pinned window' in PowerToys settings (or restyle color/opacity/thickness/rounded corners) before recording.

> Verbatim from the docs' canonical GitHub source (ms.date 08/20/2025): 'When you activate Always On Top (default: Win+Ctrl+T), the utility pins the active window above all other windows. The pinned window stays on top, even when you select other windows.' Border default confirmed by fetching live PowerToys source constants. Chromium compatibility supported indirectly by PowerToys issue #23766 (a Chrome window stayed pinned — i.e., pinning works on Chromium windows). Minor operational notes: elevated windows require PowerToys run elevated; a 'do not activate in Game Mode' setting exists.

Sources: https://learn.microsoft.com/en-us/windows/powertoys/always-on-top · https://raw.githubusercontent.com/microsoft/PowerToys/main/src/settings-ui/Settings.UI.Library/AlwaysOnTopProperties.cs

## Refuted in verification (do not act on these)

- **[1-2] REFUTED:** Devpost online judging is scored per-criterion with 1-5 star ratings in a 'Rate the Submission' panel on each submission's gallery page — so Trace's four weighted criteria (Innovation 30%, Technical Depth 30%, Problem Value 25%, Presentation 15%) will each be reduced to a 1-5 star click, meaning the video and text description must make each criterion independently and quickly scorable. [Quote reco

- **[0-3] REFUTED:** pywebview's transparent window option does NOT work on Windows, so a truly transparent floating orb over Revit is not achievable with pywebview on the demo machine; only chrome-hiding via frameless is possible.


## All sources consulted

- https://uxdesign.cc/where-should-ai-sit-in-your-ui-1710a258390e
- https://m3.material.io/styles/motion/easing-and-duration
- https://www.joshwcomeau.com/animation/linear-timing-function/
- https://animations.dev/learn/animation-theory/the-easing-blueprint
- https://learn.microsoft.com/en-us/microsoft-cloud/dev/copilot/isv/ux-guidance
- https://uiverse.io/challenges/voice-assistant-orb
- https://www.nngroup.com/articles/less-chat-more-answer/
- https://www.intercom.com/help/en/articles/13177409-customize-fin-ai-agent-tone-of-voice-and-answer-length
- https://www.intercom.com/help/en/articles/10560969-fin-guidance-best-practices
- https://thefrontkit.com/blogs/ai-chat-ui-best-practices
- https://www.parallelhq.com/blog/chatbot-ux-design
- https://mobbin.com/glossary/empty-state
- https://info.devpost.com/blog/hackathon-judging-tips
- https://info.devpost.com/blog/6-tips-for-making-a-hackathon-demo-video
- https://help.devpost.com/article/103-how-to-judge-an-online-hackathon
- https://info.devpost.com/blog/understanding-hackathon-submission-and-judging-criteria
- https://github.com/r0x0r/pywebview/issues/1611
- https://github.com/r0x0r/pywebview/issues/745
- https://learn.microsoft.com/en-us/windows/powertoys/always-on-top
- https://pywebview.flowrl.com/api/
- https://gist.github.com/YoRyan/6b4d629cca7422d15f93754938168fb7
- https://developer.chrome.com/docs/ai/render-llm-responses
- https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events