## SUMMARY
The "Design Brief Memory Agent" targets a genuinely expensive and well-documented set of AEC failures, and the evidence base is strong enough to quote directly to industry buyers. The single most powerful frame is the UK's post-Grenfell "golden thread of information" — now statutory under the Building Safety Act 2022 — because Dame Judith Hackitt's 2018 review explicitly named the exact problem this product solves: "Why design and construction decisions were made, and by whom, may not be recorded." That converts a "nice-to-have knowledge tool" into a regulatory-compliance and professional-liability instrument for higher-risk buildings. [web search — Hackitt report, ICE, gov.uk]

The cost evidence is equally concrete. The 2018 FMI/PlanGrid/Autodesk "Construction Disconnected" study put US non-productive labor (searching for information, conflict resolution, rework) at ~$177B/year, with ~$31B/year of that being rework caused specifically by miscommunication and bad/inaccessible data, and found that 48% of all rework traces to poor communication and poor project information — i.e. the documentation gap this agent closes. The UK Get It Right Initiative (GIRI) puts avoidable error at ~21% of project cost (£10–25B/year). The Construction Industry Institute pegs direct field rework at ~5% of project cost (range 2–20%). The Navigant Construction Forum's RFI study (1,362 projects, >1M RFIs) found ~$1,080 to process each RFI and ~9.9 RFIs per $1M of project value, with roughly 1 in 4 RFIs never answered. [web search — multiple]

The "why is this hard" story is fragmentation and personnel churn: a Levitt Bernstein architect's line "it's quite likely that nobody who is there at the very beginning of a project is involved at the end" captures the tribal-knowledge problem precisely, and the "or equivalent" material-substitution loophole shows how documented design intent gets silently reversed during value engineering. A 2025 ITcon academic paper frames the core gap cleanly: current practice records what was designed but not why, so teams lose the rationale and re-litigate rejected alternatives. The macro backdrop is McKinsey's "Reinventing Construction" ($1.6T productivity opportunity; construction labor productivity grew only ~1%/yr vs 2.8% economy-wide). Confidence is high on the regulatory/Hackitt and McKinsey material and medium on vendor-reported cost figures (verify primary reports before publishing exact numbers).

## KEY FINDINGS
- **[high]** Hackitt's post-Grenfell review named the exact problem this agent solves: design decisions and their authorship go unrecorded.
  - evidence: Building a Safer Future (May 2018): 'Why design and construction decisions were made, and by whom, may not be recorded, and the final records of the design may not reflect what has actually been built.' Led to the statutory 'golden thread of information' for higher-risk buildings under the Building Safety Act 2022.
  - source: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/707785/Building_a_Safer_Future_-_web.pdf
- **[medium]** Bad data and miscommunication cost the US construction industry ~$177B/year in non-productive labor, of which ~$31B/year is rework.
  - evidence: FMI/PlanGrid/Autodesk 'Construction Disconnected' (2018, ~600 leaders surveyed): 35% of time / ~14 hrs/week on non-productive work = >$177B US labor cost in 2018; rework from miscommunication and inaccurate/inaccessible data = >$31B (poor communication $17B + poor project data $14.3B).
  - source: https://www.autodesk.com/blogs/construction/survey-plangrid-fmi/
- **[medium]** Nearly half of all construction rework is caused by the information/documentation gap this product addresses.
  - evidence: 'Construction Disconnected': miscommunication and poor project data account for 48% of all rework — 26% from poor communication between team members, 22% from poor project information (erroneous data, difficulty accessing data, inability to share).
  - source: https://www.autodesk.com/blogs/construction/construction-disconnected-fmi-report/
- **[medium]** In the UK, avoidable error runs to ~21% of project cost, far above older 5% estimates.
  - evidence: Get It Right Initiative (GIRI): true avoidable error cost ~21% (~£21B/year); total cost of error incl. indirect/latent ranges 10–25% of project cost (£10–25B/year across UK construction).
  - source: https://getitright.uk.com/
- **[medium]** Direct field rework alone averages ~5% of total project cost.
  - evidence: Construction Industry Institute (CII, IR-153): direct field rework averages ~5% of total project costs, ranging 2–20% by project type; broader studies cluster at 4–12%.
  - source: https://www.openspace.ai/blog/cost-of-rework-in-construction/
- **[medium]** RFIs are frequent and expensive, and a large share go unanswered — symptomatic of undocumented decisions.
  - evidence: Navigant Construction Forum RFI study (1,362 projects, >1M RFIs): ~$1,080 average cost to process one RFI; ~9.9 RFIs per $1M of project value; ~9.7 days average to close; nearly 1 in 4 RFIs receive no reply.
  - source: https://esub.com/blog/rfi-cost-construction-firm
- **[high]** Project knowledge walks out the door — fragmentation across the project lifecycle is the core failure mode.
  - evidence: Levitt Bernstein architect Jo McCafferty (AJ roundtable on Hackitt's golden thread): 'It's quite likely that nobody who is there at the very beginning of a project is involved at the end.' Hackitt: information is 'often fragmented, incomplete and held by a number of different parties, some of whom will no longer be involved' after handover.
  - source: https://www.architectsjournal.co.uk/news/roundtable-what-do-architects-think-of-hackitts-golden-thread-of-design-intent
- **[medium]** Documented design intent gets silently reversed during construction via material substitution.
  - evidence: AJ roundtable: architects flag the broad 'or equivalent' clause contractors use to swap specified products for cheaper alternatives even where materials were chosen for environmental/thermal performance or longevity — intent lost without a decision trail.
  - source: https://www.architectsjournal.co.uk/news/roundtable-what-do-architects-think-of-hackitts-golden-thread-of-design-intent
- **[medium]** Industry research confirms the gap is recording 'what' but not 'why' — exactly the decision+reason+timestamp the agent captures.
  - evidence: ITcon Vol.30 (May 2025), Wyke et al., 'Understanding Design Rationale and Intent': a project needs both explicit design rationale and intent to succeed; current practice captures what was designed but neglects why, so teams lose reasoning and repeat rejected alternatives.
  - source: https://www.itcon.org/paper/2025/26
- **[high]** Macro backdrop: construction is a chronic productivity laggard with a $1.6T improvement prize.
  - evidence: McKinsey Global Institute 'Reinventing Construction' (Feb 2017): closing the productivity gap would add ~$1.6T/year (~2% of global economy); construction labor productivity grew ~1%/yr over two decades vs 2.8% total economy and 3.6% manufacturing.
  - source: https://www.mckinsey.com/capabilities/operations/our-insights/reinventing-construction-through-a-productivity-revolution
- **[low]** A large share of RFIs and change orders originate in design documentation gaps, not field conditions.
  - evidence: Vendor/industry analyses: ~70% of RFIs attributed to design errors, incomplete drawings, or missing specs; a major US developer found ~1/3 of change orders came from design errors and omissions; E&O change orders cited at ~3–5% of construction budget. (Secondary, methodology not standardized.)
  - source: https://www.qecad.com/cadblog/why-most-rfis-originate-in-construction-documentation-and-not-in-design/
- **[low]** Design errors and omissions are a leading driver of architect/engineer professional-liability (E&O) claims, tying documentation to legal exposure.
  - evidence: A&E professional liability claims commonly arise from mistakes/omissions in design documents (e.g., omitted fire-safety specifications, miscalculated loads); settlements reach hundreds of thousands to millions. No single agreed % of claims found in sources.
  - source: https://www.berkleydp.com/architects-engineers-claim-scenarios/

## STRUCTURED
## Pain Point 1 — Loss of design intent / design rationale between phases and into construction documents

The strongest framing is that the industry records *what* was decided but not *why*. The 2025 ITcon paper (Wyke et al., "Understanding Design Rationale and Intent," Vol.30) argues a project "must have both explicit design rationale and intent available to be successful," and that without documented rationale teams "repeat rejected alternatives and lose the reasoning behind decisions" — current practice "captures what was designed but neglects why it was designed that way." [web search — itcon.org abstract, medium confidence]

Design intent is also actively *reversed* during delivery, not merely forgotten. In the Architects' Journal roundtable on Hackitt's golden thread, architects flagged the contractual "or equivalent" clause that lets contractors substitute cheaper products for specified materials even when those materials were chosen for "environmental thermal performance or longevity" — the original rationale evaporates because no decision trail travels with the spec. They also noted cost plans are sometimes "withheld" from architects, so design decisions get unwound in commercial conversations the design team never sees. [web search — AJ roundtable, medium confidence]

Implication for the product: capturing decision + timestamp + reason and flagging when a downstream substitution contradicts the recorded rationale is exactly the unmet need named in the literature.

## Pain Point 2 — Cost of rework, design errors, and change orders (the hard numbers)

Front-line quotable statistics, with sources and confidence:

- FMI / PlanGrid / Autodesk, "Construction Disconnected" (2018, ~600 industry leaders): non-productive activities (looking for project info, conflict resolution, rework) consume ~35% of workers' time (>14 hrs/week) = **>$177B in US construction labor cost in 2018**. Rework caused by miscommunication and inaccurate/inaccessible information = **>$31B/year** (poor communication $17B + poor project data $14.3B). **48% of all US jobsite rework** traces to poor communication (26%) and poor project information (22%). [medium — Autodesk/PlanGrid press materials reporting the FMI study]
- A 2021 Autodesk/FMI follow-up ("Harnessing the Data Advantage") headlined that better data strategies could save global construction **~$1.85 trillion**. [low-medium — saw title only, verify before quoting]
- Construction Industry Institute (CII, IR-153): **direct field rework ~5% of total project cost** (range 2–20% by type). Broader literature clusters at 4–12% of project value; some UK figures higher. [medium]
- UK Get It Right Initiative (GIRI): avoidable error **~21% of project cost (~£21B/year)**; total cost of error including indirect/latent defects **10–25% / £10–25B/year**. GIRI explicitly argues the real number is far above the older 5% international estimate. [medium]
- McKinsey "Reinventing Construction" (Feb 2017): the **$1.6 trillion/year** productivity prize; construction labor productivity grew only **~1%/yr** over two decades vs **2.8%** total economy and **3.6%** manufacturing — context for why information waste persists. [high]
- Change orders / overruns: vendor and academic compilations cite average cost overrun ~28% and ~85% of projects exceeding budget (echoes Flyvbjerg megaproject data); E&O-driven change orders ~3–5% of budget; ~60% of projects over budget due to scope changes. Treat the overrun percentages as **low–medium** confidence — methodology varies widely and several trace to vendor blogs rather than primary research.

Honest caveat: the rework percentages span 2–30% across sources because of differing definitions (direct vs indirect, field vs design, region). The defensible primary anchors are CII (~5% direct field rework) and GIRI (~21% avoidable error, UK). The $177B/$31B FMI figures are the most quotable but are reported via Autodesk/PlanGrid, not an independent primary I could open directly (their blog returned HTTP 403).

## Pain Point 3 — Design brief drift / scope creep / evolving requirements

Scope change is repeatedly identified as the single largest source of change on projects (the Construction Institute calls modification of scope "the single most common source of change"). Reported figures: ~60% of projects go over budget due to scope changes; average overrun attributed to scope creep ~27%; ~85% of projects experiencing scope creep exceed budget. [low–medium — these come from scope-creep aggregator/vendor sites; the underlying overrun data partly derives from Flyvbjerg's academic work but the specific percentages should be verified before publication.]

The mechanism the agent addresses: requirements evolve meeting-to-meeting, but the *brief* (the contractual statement of client requirements) is rarely re-baselined or version-controlled, so drift is detected late — typically as a change order or RFI during construction rather than at the design stage where it is cheap to absorb.

## Pain Point 4 — Information management failure: fragmentation, tribal knowledge, people leaving

This is the emotional core and is exceptionally well evidenced from the Hackitt review itself:

- Hackitt, "Building a Safer Future" (May 2018): information "is often fragmented, incomplete and held by a number of different parties, some of whom will no longer be involved once the asset has been built and handed over. **Why design and construction decisions were made, and by whom, may not be recorded**, and the final records of the design may not reflect what has actually been built." [high — government report]
- AJ roundtable, Jo McCafferty (Levitt Bernstein): "**It's quite likely that nobody who is there at the very beginning of a project is involved at the end.**" [high — directly attributed quote]
- The records live across email, meeting minutes, drawing markups, and BIM models with no single system of record; design-intent best-practice guidance now explicitly recommends that "every decision should live in a single system of record, with changes linked back to the original design intent and rationale documented rather than assumed." [medium]
- Tribal-knowledge research (manufacturing context, transferable rather than construction-specific): ~70% of critical operational knowledge is never written down and is lost when staff leave; estimated knowledge-gap cost ~$47M/org/year. Use as analogy only — mark **low** confidence for direct construction applicability.

This is the "why did we decide X?" problem stated almost verbatim in the user's brief — and the government has already validated it.

## Pain Point 5 — RFIs, coordination/clash issues, and undocumented decisions as root cause

- Navigant Construction Forum RFI study (1,362 projects worldwide, >1M RFIs): **~$1,080 to process a single RFI**; **~9.9 RFIs per $1M** of project value; **~9.7 days** average from creation to close; design professionals estimate ~8 hours to receive/log/review/respond per RFI; **nearly 1 in 4 RFIs receive no reply at all**. The "$859,000 collective cost to a project" figure is also cited. [medium — landmark but widely cited via secondary sources]
- Root causes lean heavily on documentation gaps: industry analyses attribute ~70% of RFIs to design errors, incomplete drawings, or missing specs; common triggers are coordination conflicts (two drawing sets showing different dimensions for the same wall; structural beams clashing with MEP routing; elevations not matching plans) and missing/incomplete information. [low — vendor sources, non-standardized methodology]
- A reported case: a major US developer found ~1/3 of change orders originated from design errors and omissions, prompting third-party design review. [low]

Connection to the product: many RFIs and clashes are re-asks of questions that *were* answered in an earlier meeting but never written into a durable, queryable record. A decision-memory layer directly attacks the "no reply / re-ask" loop.

## Pain Point 6 — Regulatory / liability angle (the strongest differentiator)

This is where the product moves from productivity tool to compliance instrument.

- Grenfell Tower fire (June 2017, 72 deaths) → Dame Judith Hackitt's independent review → "Building a Safer Future" (May 2018) recommended a **"golden thread of information."** [high]
- Now law: the **Building Safety Act 2022** mandates the golden thread for higher-risk buildings (HRBs). The record must show **who did what, when, and why**; every entry must be **attributable to a named user, timestamped, and immutable** (historical states preserved, not overwritten). The principal designer/design team must record all fire-safety design decisions (e.g., via a master design risk register) and place key information in the Fire and Emergency File. [high — ICE / multiple compliance sources; the "named user, timestamped, immutable" requirement maps 1:1 onto a decision-memory data model]
- Professional liability: design errors and omissions are a leading driver of architect/engineer E&O claims (omitted fire-safety specs, miscalculated loads), with settlements from hundreds of thousands into the millions; AIA standard documents tie indemnification to the architect's errors and omissions. A timestamped, attributable decision audit trail is a direct defense and risk-management asset in disputes. [low–medium on specific claim percentages — no single agreed figure found; the qualitative point is well supported]

Positioning takeaway: "golden thread" is the highest-leverage wedge. The UK has legislated a requirement whose literal language — who decided, what, when, and why, immutably and attributably — is the product's data model. That converts the agent from optional to (for HRBs) effectively mandatory infrastructure, and it generalizes to professional-liability defense globally.

## Confidence summary / what to verify before publishing exact numbers
- HIGH: Hackitt quotes and golden-thread statutory requirements; McKinsey $1.6T and productivity growth rates; the qualitative fragmentation/personnel-churn narrative.
- MEDIUM: FMI $177B/$31B/48% (reported via Autodesk/PlanGrid, primary PDF not opened); CII ~5% rework; GIRI ~21%/£10–25B; Navigant RFI figures; ITcon "what not why" finding.
- LOW: scope-creep overrun percentages (28%/85%/27%), "70% of RFIs from design errors," E&O share of change orders, tribal-knowledge 70%/$47M (manufacturing analogy). Pull the original GIRI report, the FMI "Construction Disconnected" PDF, and the Navigant Construction Forum report before quoting their numbers as fact.

## SOURCES
- https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/707785/Building_a_Safer_Future_-_web.pdf
- https://www.ice.org.uk/news-views-insights/inside-infrastructure/golden-thread-through-new-building-safety-regime
- https://www.architectsjournal.co.uk/news/roundtable-what-do-architects-think-of-hackitts-golden-thread-of-design-intent
- https://www.autodesk.com/blogs/construction/survey-plangrid-fmi/
- https://www.autodesk.com/blogs/construction/construction-disconnected-fmi-report/
- https://www.autodesk.com/blogs/construction/autodesk-fmi-study-global-construction-industry-data-strategies/
- https://www.mckinsey.com/capabilities/operations/our-insights/reinventing-construction-through-a-productivity-revolution
- https://getitright.uk.com/
- https://getitright.uk.com/about
- https://www.openspace.ai/blog/cost-of-rework-in-construction/
- https://www.inspectmind.ai/resources/articles/true-cost-construction-rework
- https://esub.com/blog/rfi-cost-construction-firm
- https://www.procore.com/library/rfi-construction
- https://www.itcon.org/paper/2025/26
- https://www.qecad.com/cadblog/why-most-rfis-originate-in-construction-documentation-and-not-in-design/
- https://www.constrafor.com/the-build-up/scope-creep-in-construction-projects-by-the-numbers
- https://stopscopecreep.com/blog/scope-creep-statistics
- https://www.berkleydp.com/architects-engineers-claim-scenarios/
- https://www.aia.org/resource-center/standard-of-care-confronting-the-errors-and-omissions-taboo-up-front
- https://www.building.co.uk/news/revealed-key-principles-of-hackitts-golden-thread-to-improve-building-safety/5113007.article
- https://www.part3.io/blog/protect-design-intent-in-construction