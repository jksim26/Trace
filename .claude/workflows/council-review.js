export const meta = {
  name: 'council-review',
  description: 'Reconvene the Trace review council: 5 personas debate, disputed claims fact-checked, judge delivers verdict',
  whenToUse: 'When the user asks to reconvene the council, re-run the council review, or have the judges assess the project again (optionally against a prior review).',
  phases: [
    { title: 'Opening Statements', detail: '5 council members independently review the repo' },
    { title: 'Rebuttals', detail: 'each member challenges the others' },
    { title: 'Fact Check', detail: 'disputed claims verified against the code' },
    { title: 'Closing Statements', detail: 'final positions after the debate' },
    { title: 'Verdict', detail: 'the presiding judge synthesizes the debate' },
  ],
}

// args (all optional):
//   repoPath    — repo root (default /home/user/Trace)
//   today       — ISO date string for "today" (workflows cannot call Date.now(); pass it in)
//   deadline    — free-text deadline context shown to every member
//   priorReview — repo-relative path to a previous council review to re-review against
//   focus       — extra free-text instruction appended to every member's mandate
const REPO = (args && args.repoPath) || '/home/user/Trace'
const TODAY = (args && args.today) || '(date not provided — check `git log -1 --format=%cd` for recency context)'
const DEADLINE = (args && args.deadline) || 'Hackathon: Qwen Cloud Global AI Hackathon, Track 1 "MemoryAgent"; internal submission target 2026-07-07; hard deadline 2026-07-09 14:00 PDT.'
const PRIOR = (args && args.priorReview) || null
const FOCUS = (args && args.focus) || null

const RE_REVIEW = PRIOR
  ? `\nTHIS IS A RE-REVIEW. The council previously reviewed this repo; the full prior verdict is at ${REPO}/${PRIOR} — READ IT FIRST. Your mandate this round: judge the IMPROVEMENT. Check specifically: (1) were the prior top recommendations executed, and well? (2) are the claims previously fact-checked FALSE/PARTIAL now true, removed, or still standing? (3) did anything regress? Score the project as it stands today, but your statement must explicitly compare against the prior review.\n`
  : ''

const REPO_CONTEXT = `
PROJECT UNDER REVIEW: "Trace" at ${REPO} (a git repo) — an ambient design-decision memory agent for AEC
(architecture/engineering/construction). Today is ${TODAY}. ${DEADLINE}
${RE_REVIEW}
Orient yourself from the repo itself: README.md is the pitch; Trace/ holds the Python source and tests
(offline tests need no API key — tests requiring DASHSCOPE_API_KEY may fail and that is NOT the project's fault);
docs/ holds the strategy/architecture/pitch docs; demo/ the demo script and transcripts; .research/ the research appendix.
${FOCUS ? '\nADDITIONAL FOCUS FROM THE USER: ' + FOCUS + '\n' : ''}
You have full tool access: Read, Grep, Glob, Bash. Cite evidence as file:line wherever possible.
Your final output is machine-consumed structured data for a debate orchestrator, not a message to a human.`

const PERSONAS = [
  {
    key: 'aria',
    name: 'Aria Chen',
    title: 'The Hackathon Judge',
    lens: `You have judged dozens of AI hackathons. Evaluate ONLY through the lens of: will this win Track 1 (MemoryAgent)?
Assess: alignment with the track's stated focus (efficient memory storage/retrieval, timely forgetting, recall within limited context windows);
demo punch and legibility to a tired judge watching 100 entries; differentiation vs the typical "chatbot with a vector DB" memory-agent entry;
whether the remaining scope is finishable in the time left; single-point-of-failure demo risks (API keys, live calls, platform-specific launchers);
whether the pitch materials (docs/10-pitch-kit.md, demo/demo-script.md) actually land. Read the strategy doc (docs/03-hackathon-strategy.md) and judge whether the strategy is being executed.
Be concrete about what gains or loses points with judges.`,
  },
  {
    key: 'marcus',
    name: 'Marcus Webb',
    title: 'The Staff Engineer',
    lens: `Twenty years of code review; you are unimpressed by pitches and only trust code. Evaluate the engineering:
correctness of the bi-temporal store (store.py, schema.sql — is it actually bi-temporal? transaction-time vs valid-time handled right?),
the invalidation logic (invalidate.py, court.py — real reasoning or string matching?), retrieval (recall.py, strategies.py — is the budget enforcement real?),
capture.py, mcp_tools.py, cli.py. RUN THE TEST SUITE in a way a fresh judge would (fresh-clone semantics; note collection errors) and report actual results.
Scrutinize the tests: do they test behavior or just happy paths? Hunt for real defects: SQL quoting issues, timezone/timestamp bugs, mutable-default traps,
unhandled errors, schema mismatches, ID-generation collisions, dead code. Judge whether this architecture survives contact with real data.
Score the code as code, noting hackathon context only where fair.`,
  },
  {
    key: 'vera',
    name: 'Vera Okafor',
    title: 'The Skeptic',
    lens: `Professional debunker. Your job is the gap between what the pitch CLAIMS and what the code DOES.
For EACH judge-facing claim (README.md, docs/10-pitch-kit.md, demo/demo-script.md): read the code that supposedly implements it and document precisely
what it actually does (e.g. is invalidation LLM inference or keyword/rule matching? is capture ambient or manual ingestion of pre-written transcripts?
is "immutable" actually immutable? do the advertised retrieval components exist? are test counts accurate?).
Audit the .research/ confidence tags — spot-check whether [verified] claims are plausible. Check docs/06-open-questions.md for admitted gaps and whether external confidence matches internal honesty.
Also explicitly flag claims that ARE honest — you lose credibility in the debate if you only attack. Every accusation needs file:line evidence.`,
    // The Skeptic is the most output-heavy persona (she catalogs every claim with file:line);
    // without this guard her opening can overflow into an unparseable StructuredOutput blob and burn the retry cap.
    outputGuard: `OUTPUT DISCIPLINE (critical): emit your entire answer in ONE StructuredOutput call whose top level has EXACTLY the required keys (persona, score, headline, opening_statement, strengths, weaknesses, key_claims). Do NOT wrap it in a "raw" string, do NOT send a bare {point, evidence} fragment, and do NOT split across multiple calls. Keep opening_statement to 300-450 words; keep each strengths/weaknesses "evidence" to a single file:line phrase; cap strengths, weaknesses, and key_claims at 6 items each. Favor completeness of the object over exhaustiveness of any one field.`,
  },
  {
    key: 'sol',
    name: 'Sol Andersson',
    title: 'The Champion',
    lens: `Steelman advocate. Argue the strongest HONEST case for this project. Four skeptical colleagues will cross-examine every sentence you write,
so every point of praise must be anchored to specific files/lines or it will be used against you.
Look for: what is genuinely novel (is premise-invalidation-as-first-class-event actually rare in memory agents?); where execution exceeds hackathon standard
(test coverage, docs discipline, the confidence-tagging convention, the bi-temporal schema, the staged demo); evidence of good judgment (scope cuts, risk registers, deadline buffers);
whether the AEC vertical choice is strategically smart vs generic memory demos. Concede weaknesses preemptively where they are undeniable — a steelman that ignores flaws loses.`,
  },
  {
    key: 'ingrid',
    name: 'Ingrid Halvorsen',
    title: 'The AEC Domain Expert',
    lens: `Thirty years across architecture practice and building-compliance consulting. Evaluate domain truth:
Does the framing (design decisions lost across meetings, a cost decision silently breaking a fire decision, handover when a senior engineer leaves) match how AEC actually fails?
Is Trace/rules/fire.yaml plausible as a fire-code rulepack — are the rules real-shaped or toy, and do they faithfully encode their cited clauses? Do demo/transcripts/*.md read like real design meetings or like screenplay?
Is the UK Building Safety Act "golden thread" wedge legally accurate as characterized (docs/01-aec-direction.md)? Is the Singapore QP personal-liability angle (docs/07-singapore-angle.md) sound?
What would a real firm need before adopting this (BIM/CDE integration? liability of a false invalidation alert? who types the decisions in?), and does the roadmap acknowledge those honestly?`,
  },
]

const OPENING_SCHEMA = {
  type: 'object',
  required: ['persona', 'score', 'headline', 'opening_statement', 'strengths', 'weaknesses', 'key_claims'],
  properties: {
    persona: { type: 'string' },
    score: { type: 'number', description: 'Overall project score 1-10 from your lens' },
    headline: { type: 'string', description: 'One-sentence position' },
    opening_statement: { type: 'string', description: '300-500 word argued position, written in your persona voice, citing file:line evidence' },
    strengths: { type: 'array', items: { type: 'object', required: ['point', 'evidence'], properties: { point: { type: 'string' }, evidence: { type: 'string', description: 'file:line or concrete observation' } } } },
    weaknesses: { type: 'array', items: { type: 'object', required: ['point', 'evidence'], properties: { point: { type: 'string' }, evidence: { type: 'string' } } } },
    key_claims: { type: 'array', items: { type: 'string' }, description: '3-6 falsifiable claims you are staking your position on — colleagues will attack these' },
  },
}

const REBUTTAL_SCHEMA = {
  type: 'object',
  required: ['persona', 'rebuttal', 'challenges', 'concessions', 'factual_disputes', 'revised_score'],
  properties: {
    persona: { type: 'string' },
    rebuttal: { type: 'string', description: '250-450 word rebuttal in persona voice, engaging colleagues BY NAME' },
    challenges: { type: 'array', items: { type: 'object', required: ['target', 'their_claim', 'counter'], properties: { target: { type: 'string', description: 'colleague name' }, their_claim: { type: 'string' }, counter: { type: 'string', description: 'your counter-argument with file:line evidence' } } } },
    concessions: { type: 'array', items: { type: 'string' }, description: 'points from colleagues you now accept' },
    factual_disputes: { type: 'array', items: { type: 'object', required: ['claim', 'verification_hint'], properties: { claim: { type: 'string', description: 'a checkable factual claim about the repo that the council disagrees on' }, verification_hint: { type: 'string', description: 'which files/commands would settle it' } } } },
    revised_score: { type: 'number' },
  },
}

const VERIFY_SCHEMA = {
  type: 'object',
  required: ['claim', 'verdict', 'evidence'],
  properties: {
    claim: { type: 'string' },
    verdict: { type: 'string', enum: ['TRUE', 'FALSE', 'PARTIAL'] },
    evidence: { type: 'string', description: 'file:line citations and/or command output proving the verdict' },
    nuance: { type: 'string' },
  },
}

const CLOSING_SCHEMA = {
  type: 'object',
  required: ['persona', 'closing_statement', 'final_score', 'top_recommendation'],
  properties: {
    persona: { type: 'string' },
    closing_statement: { type: 'string', description: 'max 200 words: what you still stand by, what you concede after the fact-checks' },
    final_score: { type: 'number' },
    top_recommendation: { type: 'string', description: 'the single highest-impact thing to do next' },
  },
}

// ---- Phase 1: Opening statements (independent, parallel) ----
phase('Opening Statements')
log(`Convening the council: 5 members reviewing ${REPO} independently${PRIOR ? ' (re-review vs ' + PRIOR + ')' : ''}`)
const openings = await parallel(PERSONAS.map(p => () =>
  agent(
    `${REPO_CONTEXT}\n\nYOU ARE: ${p.name}, "${p.title}", a member of a 5-person review council. The other members are: ${PERSONAS.filter(q => q.key !== p.key).map(q => q.name + ' (' + q.title + ')').join(', ')} — they are reviewing the same repo through different lenses and will attack weak claims in your statement.\n\nYOUR LENS:\n${p.lens}\n\nExplore the repo thoroughly with your tools (read the actual source, not just the README). Then produce your structured opening. Set persona to "${p.name}". Make key_claims specific and falsifiable — vague claims will be shredded in rebuttals.${p.outputGuard ? '\n\n' + p.outputGuard : ''}`,
    { label: `opening:${p.name}`, phase: 'Opening Statements', schema: OPENING_SCHEMA, effort: 'high' }
  )
))
const validOpenings = openings.filter(Boolean)
if (validOpenings.length < 3) throw new Error('Too few opening statements survived; aborting council')
log(`Opening scores: ${validOpenings.map(o => `${o.persona} ${o.score}/10`).join(', ')}`)

// ---- Phase 2: Rebuttals (each sees all openings — barrier is genuinely required) ----
phase('Rebuttals')
const openingsDossier = JSON.stringify(validOpenings, null, 1)
const rebuttals = await parallel(PERSONAS.map(p => () => {
  const mine = validOpenings.find(o => o.persona === p.name)
  if (!mine) return Promise.resolve(null)
  return agent(
    `${REPO_CONTEXT}\n\nYOU ARE: ${p.name}, "${p.title}". Round 2 of the council debate: rebuttals.\n\nYOUR LENS (unchanged):\n${p.lens}\n\nALL FIVE OPENING STATEMENTS (including yours) as JSON:\n${openingsDossier}\n\nYour task: challenge at least 2 specific claims made by OTHER council members. Do not argue from memory — re-check the repo with your tools before contradicting a colleague; a challenge without file:line evidence is worthless. Concede points where a colleague is simply right. Where the council factually disagrees about what the code/docs contain, record it in factual_disputes so an independent fact-checker can settle it. Revise your score if colleagues changed your mind. Set persona to "${p.name}".`,
    { label: `rebuttal:${p.name}`, phase: 'Rebuttals', schema: REBUTTAL_SCHEMA, effort: 'medium' }
  )
}))
const validRebuttals = rebuttals.filter(Boolean)
log(`Rebuttals in: ${validRebuttals.length}; revised scores: ${validRebuttals.map(r => `${r.persona} ${r.revised_score}/10`).join(', ')}`)

// ---- Phase 3: Fact-check disputed claims (dedupe, cap, verify in parallel) ----
phase('Fact Check')
const seen = new Set()
const disputes = []
for (const r of validRebuttals) {
  for (const d of (r.factual_disputes || [])) {
    const k = (d.claim || '').toLowerCase().replace(/\s+/g, ' ').slice(0, 90)
    if (k && !seen.has(k)) { seen.add(k); disputes.push(d) }
  }
}
const CAP = 12
if (disputes.length > CAP) log(`Capping fact-checks at ${CAP} of ${disputes.length} disputes; dropped: ${disputes.slice(CAP).map(d => d.claim).join(' | ')}`)
const toVerify = disputes.slice(0, CAP)
log(`Fact-checking ${toVerify.length} disputed claims`)
const verifications = (await parallel(toVerify.map(d => () =>
  agent(
    `${REPO_CONTEXT}\n\nYou are an independent fact-checker for a review council. The council disputes this factual claim about the repo:\n\nCLAIM: ${d.claim}\n\nHow to settle it (hint from the council): ${d.verification_hint}\n\nAdversarially verify it against the ACTUAL repo — read the code, run commands if needed. NEVER print secret/credential values (API keys, tokens) into your output or command output; test presence with indirection (e.g. test -n) only. Do not take either side's word. Verdict TRUE (claim holds), FALSE (claim is wrong), or PARTIAL (true in part — explain the boundary in nuance). Evidence must cite file:line or command output.`,
    { label: `verify:${(d.claim || '').slice(0, 50)}`, phase: 'Fact Check', schema: VERIFY_SCHEMA, effort: 'medium' }
  )
))).filter(Boolean)
log(`Fact-check verdicts: ${verifications.map(v => v.verdict).join(', ') || 'none'}`)

// ---- Phase 4: Closing statements ----
phase('Closing Statements')
const rebuttalsDossier = JSON.stringify(validRebuttals, null, 1)
const verificationsDossier = JSON.stringify(verifications, null, 1)
const closings = (await parallel(PERSONAS.map(p => () => {
  const mine = validOpenings.find(o => o.persona === p.name)
  if (!mine) return Promise.resolve(null)
  return agent(
    `You are ${p.name}, "${p.title}", closing a 5-person council debate about the repo at ${REPO}. Today is ${TODAY}. ${DEADLINE}\n\nYOUR OPENING:\n${JSON.stringify(mine, null, 1)}\n\nALL REBUTTALS:\n${rebuttalsDossier}\n\nINDEPENDENT FACT-CHECK VERDICTS on the council's disputed claims:\n${verificationsDossier}\n\nGive your closing: what survives the debate, what you concede (especially where fact-checks went against you), your final 1-10 score, and the ONE highest-impact recommendation. Max 200 words, persona voice. Set persona to "${p.name}". No need to re-read the repo.`,
    { label: `closing:${p.name}`, phase: 'Closing Statements', schema: CLOSING_SCHEMA, effort: 'medium' }
  )
}))).filter(Boolean)
log(`Final scores: ${closings.map(c => `${c.persona} ${c.final_score}/10`).join(', ')}`)

// ---- Phase 5: The Judge ----
phase('Verdict')
const judgeReport = await agent(
  `You are the Presiding Judge of a 5-member review council that just debated the repo at ${REPO} — "Trace", a design-decision memory agent for AEC. Today is ${TODAY}. ${DEADLINE}${PRIOR ? `\nTHIS IS A RE-REVIEW: the prior council verdict is at ${REPO}/${PRIOR} — read it, and your report must include an "Improvement since the last review" section: prior recommendations executed vs ignored, previously-FALSE claims now true/removed/standing, score delta with justification.` : ''} You may consult the repo yourself with your tools to break ties, but the debate record is your primary evidence.\n\nTHE FULL DEBATE RECORD:\n\n=== OPENING STATEMENTS ===\n${openingsDossier}\n\n=== REBUTTALS ===\n${rebuttalsDossier}\n\n=== INDEPENDENT FACT-CHECK VERDICTS ===\n${verificationsDossier}\n\n=== CLOSING STATEMENTS ===\n${JSON.stringify(closings, null, 1)}\n\nDeliver the council's final judgment as a complete markdown report (this text IS the deliverable — return only the markdown, no preamble):\n\n# The Council's Verdict on Trace\n1. **Executive verdict** — 3-5 sentences, decisive, with a final overall score /10.\n2. **Scorecard** — a table: dimension (Concept & novelty, Engineering quality, Pitch honesty, Domain fit, Hackathon readiness), score /10, one-line rationale. Derive scores from the debate, weighting fact-checked evidence over rhetoric.\n3. **Where the council agreed** — the consensus findings.\n4. **The sharpest disagreements — and who won** — for each major clash, name the members, state both positions, and rule on it citing the fact-check verdicts.\n5. **Claims that did not survive fact-checking** — pitch/code claims proven FALSE or PARTIAL, with the evidence.\n6. **Top 5 recommendations** — ranked by impact, each with effort estimate (hours) and which council member championed it.\n7. **The one-line summary** a judge would write on the scorecard.\n\nRule decisively — where members disagreed and the fact-check settled it, say who was right. Do not average scores mechanically; weigh argument quality.`,
  { label: 'judge:presiding', phase: 'Verdict', effort: 'xhigh' }
)

return { openings: validOpenings, rebuttals: validRebuttals, verifications, closings, judgeReport }
