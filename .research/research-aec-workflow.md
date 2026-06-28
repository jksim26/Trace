## SUMMARY
The AEC (Architecture, Engineering, Construction) industry runs design through formal, gated stages — the RIBA Plan of Work (Stages 0-7) in the UK/Commonwealth and the AIA phases (SD, DD, CD, CA, plus Bidding) in the US. At each stage a defined "Information Exchange" / deliverable set freezes the current state of the design and hands it to the next stage. The project brief is the spine: it starts as a Strategic Brief, becomes a Project Brief, and decomposes into an area schedule (schedule of accommodation), room data sheets (RDS), design criteria and performance specifications. Crucially, the brief is not static — it evolves as design decisions are made, and the gap between "what the brief now requires" and "what the drawings/models/specs currently say" is exactly where projects bleed money. [verified across RIBA, AIA, and Designing Buildings sources]

Design decisions live scattered across many documents: meeting minutes / design review records, RFIs, change orders, construction change directives, design change notices, value-engineering logs, derogations/concessions, NCRs, and transmittals. The industry has a clear analogue to software's "Architecture Decision Record" — the project-management "decision log / decision register" — but, unlike ADRs in software, there is NO widely-adopted, formal, standardized "design decision log" embedded in AEC design coordination. Decision logs are recommended PM practice and exist on well-run projects, but in design they are inconsistently kept; the rationale behind decisions typically lives in email, verbal agreement, or whoever happened to take minutes. This is the core pain our product targets. [inference + web-search; medium confidence]

The information-management backbone is now standardized: ISO 19650 governs information management over the asset lifecycle, defining the EIR/Exchange Information Requirements, the BIM Execution Plan (BEP), the MIDP/TIDP delivery plans, and the Common Data Environment (CDE) with its WIP -> Shared -> Published -> Archived states. Post-Grenfell, the UK Building Safety Act 2022 mandates a "golden thread" of accurate, accessible, structured safety-critical information for higher-risk buildings (>=18m or >=7 storeys with >=2 dwellings), with Gateways (notably Gateway 2 before construction) that hard-stop a project if information is incomplete. [verified — Wikipedia/ISO + UK gov/CLC sources]

Decisions cross many disciplines — client/employer, architect, structural, MEP/building services, fire, facade, civil, QS/cost, contractor and specialist sub-consultants — and a single change (parking count, facade material, floor-to-floor height, core location, structural grid) cascades across all of them, invalidating downstream area schedules, structural sizing, MEP routing, fire strategy, planning/Building-Control approvals, cost plans and programme. The 'structured' field below gives a stage-by-stage map, a full glossary, a stakeholder/decision-flow map, and four demo-ready worked examples of an evolving decision and exactly what it makes obsolete.

## KEY FINDINGS
- **[high]** AEC design is gated: RIBA Plan of Work 2020 has 8 stages (0 Strategic Definition, 1 Preparation & Briefing, 2 Concept Design, 3 Spatial Coordination, 4 Technical Design, 5 Manufacturing & Construction, 6 Handover, 7 Use); each stage ends with a defined Information Exchange that 'captures decisions made during the stage and provides the basis for the next stage'.
  - evidence: RIBA: 'The Plan of Work defines key Information Exchanges at the end of each stage... capture decisions made during the stage'; Stage 0 and Stage 7 were added in 2020.
  - source: https://www.riba.org/work/insights-and-resources/riba-plan-of-work/
- **[high]** The US/AIA equivalent runs SD (Schematic Design) -> DD (Design Development) -> CD (Construction Documents) -> Bidding/Negotiation -> CA (Construction Administration); the owner formally approves at the end of SD and DD before the next phase proceeds.
  - evidence: AIA 'Five Phases of Architecture: Schematic Design, Design Development, Contract [Construction] Documents, Bidding, Contract [Construction] Administration'; 'The owner approves these sketches before proceeding'.
  - source: https://www.aia.org/resource-center/defining-the-architects-basic-services
- **[high]** The brief is a living spine that decomposes into area schedule (schedule of accommodation) and room data sheets (RDS); RDS start as the client's needs and are 'taken on and developed by the design team' through DD into construction docs.
  - evidence: Designing Buildings: RDS 'can be prepared by the client in the first instance, and then taken on and developed by the design team'; covers finishes, MEP services, electrical, FF&E, dimensions, occupancy, fire, structural requirements.
  - source: https://www.designingbuildings.co.uk/wiki/Room_data_sheet
- **[high]** Design changes get exponentially more expensive the later they occur — this is the central economic argument for early decision capture.
  - evidence: Designing Buildings change-control: 'the later in the development of the project that changes occur, the greater those impacts are likely to be'; brief is 'frozen' at end of Concept Design, post-contract changes become 'variations'.
  - source: https://www.designingbuildings.co.uk/wiki/Change_control_procedure_for_building_design_and_construction
- **[medium]** Decisions are systematically lost at phase transitions and personnel changes; they live in unreliable stores (email, verbal, ad-hoc minutes) with no designated owner of the decision record.
  - evidence: Datum Notes: four failure modes — wrong storage (email/verbal), implicit-not-explicit decisions, no accountability owner, and 'phase transition gaps' where 'new consultants... work from their interpretation of the drawings rather than the documented rationale'.
  - source: https://www.datumnotes.com/resources/blog/why-architecture-projects-lose-decisions
- **[medium]** AEC has NO formal, standardized 'design decision log' embedded in design coordination the way software has ADRs; decision logs are recommended PM practice but inconsistently applied — a genuine product gap.
  - evidence: Decision-log guidance is generic PM ('used across various industries, from IT and construction'); software ADR pattern is formalized (Nygard 2011) but the construction search returned 'general project management decision logs rather than construction-industry-specific implementations'.
  - source: https://www.projectmanagertemplate.com/post/decision-logs-the-ultimate-guide
- **[high]** ISO 19650 is the standardized information-management backbone: EIR (Exchange/Employer's Information Requirements) -> BEP (BIM Execution Plan) -> MIDP/TIDP delivery plans, all governed in a CDE with WIP/Shared/Published/Archived states.
  - evidence: 'Part 2 introduces the BIM Execution Plan (BEP), Master Information Delivery Plan (MIDP) and Task Information Delivery Plans (TIDPs)'; CDE states 'Work in Progress (WIP), Shared, Published, and Archived'.
  - source: https://en.wikipedia.org/wiki/ISO_19650
- **[high]** The 'golden thread' is a legal requirement (UK Building Safety Act 2022, from the 2018 Hackitt review post-Grenfell): a digital, structured, persistent record of safety-critical information for higher-risk buildings (>=18m / >=7 storeys, >=2 dwellings).
  - evidence: Hackitt review concluded 'information critical to safe design... was systematically missing, inconsistent, or inaccessible'; BSA became law 2022; HRB defined as '18 metres or seven storeys or more... at least two residential units'.
  - source: https://www.constructionleadershipcouncil.co.uk/wp-content/uploads/2024/08/CLC-Golden-Thread-Guidance.pdf
- **[high]** Construction defines distinct change instruments with precise meanings: RFI (asks for clarification, authorizes nothing), Change Order (signed, actually amends the contract), CCD/Construction Change Directive (directs work before price agreed), derogation/concession (approved deviation from spec), NCR (non-conformance), transmittal (proof-of-delivery record of documents).
  - evidence: 'An RFI asks for clarification but doesn't authorize any changes. Only a signed change order actually amends the agreement'; derogation 'enables a party... to propose an alternative approach that deviates from the original contract requirements'.
  - source: https://metroun.co.uk/construction-law/derogations/
- **[low]** A single design change cascades across disciplines; MEP coordination is the most clash-prone interface and a leading rework cause.
  - evidence: Web-search claims (single-source, treat as indicative): 'MEP-related conflicts account for 40% of all construction RFIs', 'average MEP clash reaching the field costing $4,200 to resolve'; CDE federated models used to catch hard/soft/time clashes early.
  - source: https://helonic.com/blog/mep-coordination-best-practices
- **[medium]** Brief/floorplate economics are measured by area metrics: GIA (gross internal area) vs NIA (net internal area); NIA/GIA efficiency is a core financial KPI, so any change touching circulation/core/structure changes the appraisal.
  - evidence: Designing Buildings/industry: efficiency bands roughly 'Excellent NIA 84-87% of GIA, Good 80-83%, Poor below 80%'; commercial rent is set per sq ft of NIA. (band figures single-source, treat as indicative).
  - source: https://www.designingbuildings.co.uk/wiki/Net_internal_area_NIA
- **[medium]** Facade material change is a high-blast-radius decision post-Grenfell: it hits structural dead load and fixings, fire compliance (A1/A2-s1,d0 over 18m, cavity barriers), thermal/energy model, cost (can be 1.5-2x), and triggers Building Control / Gateway 2 re-submission.
  - evidence: 'Buildings over 7 storeys must use non-combustible cladding materials rated A1 or A2-s1,d0... entire cladding assemblies including insulation, fixings, membranes, and cavity barriers'; cost '1.5x-2x'. (cost multiple single-source, indicative).
  - source: https://ams-wa.com/fire-safety-facade-regulations/

## STRUCTURED
## 1. THE DESIGN BRIEF — what it contains and how it evolves

The brief is the project's source of truth for *intent* and *requirements*. It evolves through named versions, and each design decision should (in theory) be reconciled back to it.

**Evolution of the brief (RIBA framing):**
- **Strategic Brief** (Stage 0) — business case, high-level need, "is a building even the right answer?", site/budget envelope, strategic objectives.
- **Project Brief / Initial Project Brief** (Stage 1) — the formal requirements document; frozen as a baseline at end of Stage 2 (Concept Design). After this, changes go through *change control*.
- **Employer's Requirements (ER)** — on Design-and-Build contracts, the client's specification of what is needed; the contractor replies with **Contractor's Proposals**. ERs contain: project overview & scope of services, site information + existing drawings/BIM, programme/phasing, form of contract, prescriptive *or* performance specifications, elements requiring contractor design, inspection/testing/commissioning/handover procedures, contract-sum-analysis format, statutory-approvals responsibility, warranties/insurance, risk allocation, client policies (environmental, H&S), and the EIR/BIM protocol. [Designing Buildings]

**Brief sub-documents (the structured data inside the brief):**
- **Schedule of Accommodation / Area Schedule** — list of every required space with target areas; rolls up to **GIA** (gross internal area) and **NIA** (net internal area). NIA/GIA "efficiency" is a key financial KPI (industry bands ~80-87% good/excellent; below 80% poor — single-source, indicative).
- **Room Data Sheets (RDS)** — one page (or DB record) per room/space type: finishes (walls/floors/ceilings/doors/ironmongery/acoustics), MEP services (heating/cooling/ventilation/plumbing), electrical (outlets/lighting/sensors/data/controls), FF&E, dimensions, occupancy, fire protection, structural requirements. Start as client need, developed by design team, audited against by contractor at handover.
- **Design Criteria** — quantified targets (occupancy densities, environmental setpoints, daylight, acoustic ratings, loadings, accessibility).
- **Performance Specifications** vs **Prescriptive Specifications** — "achieve X" vs "use product Y".

---

## 2. STAGE-BY-STAGE MAP (RIBA 0-7 mapped to AIA phases) with the decisions made and where they get lost

| RIBA stage | AIA phase (approx) | Core decisions made here | Information Exchange / deliverable | Where decisions get LOST in the next transition |
|---|---|---|---|---|
| **0 Strategic Definition** | (Pre-design) | Build vs not-build; business case; site; strategic budget; key outcomes | Business Case, Strategic Brief | Strategic constraints (why a budget cap, why this site) drop out — later teams treat them as arbitrary |
| **1 Preparation & Briefing** | Programming/Pre-design | Project Brief; spatial requirements; procurement route; **EIR**; sustainability/BREEAM/LEED targets; project budget | Project Brief, Feasibility Studies, **EIR**, Project Budget | Brief rationale lives in workshops/emails; the *why* behind room counts/adjacencies isn't carried forward |
| **2 Concept Design** | **Schematic Design (SD)** | Massing, form, core location (concept), structural concept, MEP strategy, facade concept, **brief FROZEN as baseline**, cost plan 1 | Concept Design report + outline specs; **owner sign-off**; change control begins | The frozen brief vs concept drawings diverge silently; assumptions ("plant on roof", "naturally ventilated") not logged |
| **3 Spatial Coordination** | **Design Development (DD)** | Grid finalized, floor-to-floor heights, riser/shaft sizes, fire strategy, facade system, coordinated MEP zones, planning submission | Coordinated/spatially-resolved design; planning application; cost plan 2 | **Planning pause** between 3 and 4 — decisions made to win planning (heights, materials, parking) become conditions that later teams forget are binding |
| **4 Technical Design** | **Construction Documents (CD)** | Detailing, connections, specialist/sub-contractor design (facade, structure), derogations, full specs | Building Regs/Building Control + **Gateway 2** (HRBs); tender/Contract Documents | Specialist sub-consultant designs introduced; original design intent reinterpreted; "design change notices" not reconciled to brief |
| **5 Manufacturing & Construction** | **Construction Administration (CA)** + Bidding | RFIs, change orders, CCDs, substitutions, VE on site, NCRs | As-constructed information; RFI/CO logs | Site decisions (substitutions, VE) never flow back to update the model/brief/golden thread |
| **6 Handover** | Closeout | Snagging/defects, commissioning, O&M | Building manual, H&S file, **golden thread** record | Decision rationale rarely captured in O&M; "as-built" ≠ "as-decided" |
| **7 Use** | (Post-occupancy) | Operation, POE, future-change baseline | Feedback, asset information | Original constraints lost; refurb teams start blind |

**Generalized "design decision" by stage:** Stage 0-1 = *strategic/requirement* decisions (how many beds, what budget). Stage 2-3 = *spatial/system* decisions (where the core goes, grid, floor-to-floor, facade system) — these are the highest-blast-radius. Stage 4 = *technical/detail* decisions (connection types, derogations). Stage 5 = *reactive* decisions (RFIs, change orders, substitutions). The cruelest losses happen at: (a) the **Concept->Coordination brief freeze**, (b) the **planning pause (3->4)**, and (c) the **design->construction handover (4->5)** where new parties join.

---

## 3. KEY DOCUMENTS WHERE DECISIONS LIVE (and how well they capture rationale)

- **Meeting minutes / design review records** — primary contemporaneous record; treated as legally significant ("assumed accurate... agreed to by all parties"). But decisions are often *implicit* — discussions "drift toward conclusions without someone explicitly stating the final decision." Note-taking depends on whoever had time.
- **RFI (Request for Information)** — formal clarification request; authorizes nothing. RFI log is a contract artifact. (Web-search: MEP ~40% of RFIs — indicative.)
- **Change Order (CO)** — signed amendment to contract scope/cost/time; the *only* instrument that actually changes the contract.
- **Construction Change Directive (CCD)** — directs work to proceed before price is agreed (US).
- **Design Change Notice / Change Request** — internal pre-contract change instrument; routed through **change control** (record reason, requestor, impacts on H&S/time/quality/cost, mitigation, risk, alternatives, deadline -> client value-for-money decision -> instruction).
- **Value-Engineering (VE) log** — record of cost-reduction substitutions/alternatives proposed (often by contractor) "without sacrificing quality."
- **Derogation / Concession** — *approved* deviation from the spec/ER when strict compliance is impractical (material unavailable, non-compliant, unsuitable). "Project brief derogations" is a recognized Designing Buildings term.
- **NCR (Non-Conformance Report)** — QA/QC record that built work doesn't match spec; disposition decided (accept/rework/reject).
- **Transmittal** — proof-of-delivery record (who sent what to whom, when); works with **drawing registers/logs** for document control.
- **EIR + BEP + MIDP/TIDP** — information-requirement and delivery-planning documents (ISO 19650).
- **Decision Log / Decision Register** — the closest thing to a formal home for decisions: Decision ID, date, summary, decision-makers, rationale, impact, status (pending/approved/rejected), action items. **BUT: this is generic PM practice, not an AEC-design-specific standard.** Software has the formalized ADR (Architecture Decision Record, Nygard 2011); AEC has *no equivalent embedded standard* in design coordination — adoption is patchy and rationale routinely vaporizes. **This is the product opportunity.**

---

## 4. STAKEHOLDERS / DISCIPLINES and how decisions cross between them

**Parties:** Client/Employer (and end-users/operator); Architect (lead designer); Structural engineer; MEP / building-services engineer (mechanical, electrical, public-health/plumbing); Fire engineer; Facade engineer/consultant; Civil engineer (drainage, roads, externals); QS / cost consultant; Principal Designer & Principal Contractor (CDM/BSA dutyholders); Main contractor + specialist sub-contractors/trade contractors; sub-consultants (acoustics, vertical transport/lifts, sustainability, geotech, planning consultant, BIM manager/Information Manager).

**How decisions cross disciplines:** through the **CDE** (federated BIM models, ISO 19650 WIP->Shared->Published->Archived), coordination/clash-detection sessions (hard/soft/time clashes), design review meetings, RFIs, transmittals, and change control. The architect typically owns design intent; the QS prices impacts; the structural/MEP engineers must re-validate; fire and Building Control gate compliance; the contractor executes. A change "owned" by one discipline almost never stays contained — e.g., an architect moving a wall forces MEP re-routing and re-approval. The recurring failure: **changes propagate physically (the model updates) but the *decision and its rationale* don't propagate to every affected party or back to the brief.**

---

## 5. GLOSSARY (AEC terms our product must use correctly)

- **RIBA Plan of Work** — UK framework, 8 stages 0-7. **AIA phases** — US: SD/DD/CD/Bidding/CA.
- **Information Exchange** — defined deliverable set at end of each RIBA stage.
- **Strategic Brief / Project Brief / Initial Project Brief** — evolving requirement document.
- **Employer's Requirements (ER) / Contractor's Proposals** — D&B contract pair.
- **Schedule of Accommodation / Area Schedule** — required spaces + areas.
- **GIA / NIA / GEA** — gross internal / net internal / gross external area; **net-to-gross efficiency**.
- **Room Data Sheet (RDS)** — per-space spec record.
- **Performance vs Prescriptive specification.**
- **Design freeze / baseline** — point after which change control applies (end of Concept/SD).
- **Change control** — formal process to raise/assess/approve/record changes.
- **RFI** — Request for Information (clarification, no authority).
- **Change Order (CO) / Variation** — contractual change (pre-contract: change; post-contract: variation).
- **CCD** — Construction Change Directive.
- **Design Change Notice / Change Request** — design-stage change instrument.
- **Value Engineering (VE)** — cost-reduction without quality loss.
- **Derogation / Concession** — approved deviation from spec/brief.
- **NCR** — Non-Conformance Report.
- **Transmittal** — document-delivery proof; **Drawing Register** — document control list.
- **Decision Log / Decision Register** — record of decisions + rationale + status. **ADR** — software analogue (Architecture Decision Record).
- **ISO 19650** — information-management standard.
- **EIR** — Exchange/Employer's Information Requirements.
- **BEP** — BIM Execution Plan. **MIDP / TIDP** — Master / Task Information Delivery Plan.
- **CDE** — Common Data Environment (WIP / Shared / Published / Archived).
- **Golden Thread** — BSA 2022 mandated persistent safety-critical information record.
- **HRB** — Higher-Risk Building (>=18m or >=7 storeys, >=2 dwellings).
- **Gateways** — BSA hard-stop approval points (Gateway 1 planning, Gateway 2 pre-construction, Gateway 3 pre-occupation).
- **Clash detection** — hard (physical) / soft (clearance) / time (sequencing) clashes.
- **CDM / Principal Designer / Principal Contractor** — UK H&S dutyholder roles.

---

## 6. FOUR DEMO-READY WORKED EXAMPLES (a decision changes -> what it makes obsolete)

These are synthesized from the sourced cascade material — credible, but the specific downstream lists are *inference* the AEC reader will recognize, not single-source quotes.

### Example A — "Parking count 200 -> 150 (budget / VE / revised transport statement)"
*Stage: RIBA 2-3 / SD-DD. Owner: client + civil/transport; touches everyone.*
Invalidates / triggers rework in:
- **Architecture:** basement parking layout drawings; may delete a whole basement level; ramp geometry, circulation, cycle-store (planning often demands MORE cycle spaces in exchange).
- **Structural:** if a basement level is removed — foundation design, retaining walls, excavation/dewatering, basement column grid (parking grids ~7.5-8.1m differ from office/resi).
- **MEP:** car-park ventilation (CO/jet-fan) sizing, drainage/sump, lighting, EV-charging provision count.
- **Fire:** car-park smoke-extract strategy.
- **QS/cost & brief:** GIA reduction -> area schedule, cost plan, financial appraisal.
- **Planning:** transport statement / travel plan / parking condition — likely **re-approval risk** (planning condition may be breached).

### Example B — "Facade material change (e.g., brick/precast -> aluminium rainscreen, or combustible ACM -> non-combustible A2-s1,d0)"
*Stage: RIBA 4 (or post-occupancy remediation). High blast radius post-Grenfell.*
Invalidates:
- **Structural:** dead-load change -> facade support steel/brackets, slab-edge design, secondary steel; wind load on fixings re-checked.
- **Fire:** combustibility rating (A1/A2-s1,d0 over 18m), cavity barriers, fire-stopping -> **Building Control / Gateway 2 re-submission**; golden-thread record update for HRB.
- **Building physics:** U-value/thermal, condensation/interstitial-moisture analysis, Part L energy model re-run.
- **Architecture:** setting-out, floor-to-floor relationship, window reveals, weathering details, window schedule, interfaces.
- **QS/programme:** cost (cladding can be ~1.5-2x — indicative), new specialist sub-contractor package, lead times, warranties.

### Example C — "Floor-to-floor height change (3.6m -> 4.0m for services zone, OR reduced to meet a planning height cap)"
*Stage: RIBA 3 (when MEP ceiling void proves insufficient) or to meet planning envelope.*
Invalidates:
- **Planning:** overall building height -> massing, daylight/sunlight & rights-of-light, height condition — **re-approval risk**; if total height is capped, the *number of floors* may drop.
- **Brief/finance:** lost floor -> NIA/area schedule -> appraisal.
- **Structural:** column lengths/stability, wind, core/stair flights.
- **Architecture/Regs:** stair riser count & going recalculated (Part K); lift travel/shaft (lift schedule).
- **Facade:** panel module/setting-out, extra panel row -> cost.
- **MEP:** riser heights, duct drops, ceiling void re-coordination.

### Example D — "Core relocation (move lifts/stairs/risers to improve lettable floorplate)"
*Stage: RIBA 2-3. Often the single highest-impact spatial decision.*
Invalidates:
- **Structural:** the core IS the lateral-stability system (shear walls/bracing) -> stability re-design, foundation under core, transfer structure if the core no longer stacks vertically.
- **Brief/finance:** floorplate efficiency, NIA/GIA, lettable area -> financial model (the very reason for the move must be re-proven).
- **MEP:** all vertical riser distribution re-routed; drainage stacks; plant-room location.
- **Fire:** escape routes, travel distances, firefighting shaft, stair pressurization, refuges -> **Approved Doc B / Gateway re-check**.
- **Architecture/Regs:** lift strategy, lift lobby, accessibility (Part M); every floor's space plans / RDS; grid coordination.

**Demo narrative to use:** in each case the model eventually updates, but the *decision + rationale + the list of now-invalid downstream items* is what no current tool reliably holds — minutes record it implicitly, the CO records only the contractual slice, and the brief silently goes stale. A Design Brief Memory Agent that (1) captures the decision explicitly, (2) ties it to the brief item it changes, and (3) lists the downstream artifacts it invalidates is filling a real, unstandardized gap.

## OPEN QUESTIONS
- Does any specific CDE/BIM platform (Autodesk Construction Cloud, Asite, Viewpoint, Newforma, Procore) already ship a structured 'design decision register' feature, or is decision capture still bolted on via RFIs/minutes? Worth a competitive scan before the demo.
- What is the actual, current adoption rate of formal decision logs on real design projects (vs RFI/CO logs)? No hard statistic was found — claims that decisions 'live in email' are qualitative (Datum Notes), not quantified.
- The MEP-clash cost figures ($4,200/clash; MEP = 40% of RFIs) and cladding cost multiples (1.5-2x) and NIA/GIA efficiency bands are single-source web claims — verify against a primary industry study (e.g., a QS body, RICS, or academic source) before quoting in sales material.
- Exact ISO 19650-2 vocabulary for 'decision' — the standard centers on information *requirements* and *exchanges*, not decisions per se; confirm whether positioning the product as complementary-to (not competing-with) ISO 19650/CDE is the right framing.
- Building Safety Act Gateways 1/2/3 specifics and which decision types must be evidenced for Gateway 2 sign-off — confirm against the Building Safety Regulator's current guidance, as the regime has been tightening through 2024-2026.

## SOURCES
- https://www.riba.org/work/insights-and-resources/riba-plan-of-work/
- https://www.riba.org/media/syneeeto/2020ribaplanofworkoverviewpdf.pdf
- https://architectureforlondon.com/news/the-riba-plan-of-work/
- https://urbanistarchitecture.co.uk/riba-plan-of-work-stages/
- https://www.aia.org/resource-center/defining-the-architects-basic-services
- https://www.aia.org/resource-center/schematic-design-phase-quality-management
- https://www.aia.org/resource-center/managing-quality-in-the-design-development-phase
- https://monograph.com/blog/guide-to-design-phases
- https://www.designingbuildings.co.uk/wiki/Employer%27s_requirements_for_building_design_and_construction
- https://www.designingbuildings.co.uk/wiki/Room_data_sheet
- https://www.designingbuildings.co.uk/wiki/Change_control_procedure_for_building_design_and_construction
- https://www.designingbuildings.co.uk/wiki/Project_brief_derogations
- https://www.designingbuildings.co.uk/wiki/Net_internal_area_NIA
- https://en.wikipedia.org/wiki/ISO_19650
- https://catenda.com/glossary/iso-19650/
- https://www.autodesk.com/autodesk-university/article/ISO-19650-Common-Data-Environment-and-Autodesk-Construction-Cloud
- https://www.constructionleadershipcouncil.co.uk/wp-content/uploads/2024/08/CLC-Golden-Thread-Guidance.pdf
- https://www.ice.org.uk/news-views-insights/inside-infrastructure/golden-thread-through-new-building-safety-regime
- https://buildingsafety.campaign.gov.uk/building-safety-regulator-making-buildings-safer/building-safety-regulator-news/understanding-the-golden-thread/
- https://www.basystems.co.uk/blog/designing-for-compliance-how-early-stage-design-decisions-impact-gateway-2-submissions/
- https://academy2.youngarchitect.com/what-is-an-rfi-construction/
- https://www.procore.com/library/rfi-construction
- https://www.rhumbix.com/blog/what-is-change-order-construction
- https://www.newforma.com/what-is-a-construction-change-directive-ccd/
- https://metroun.co.uk/construction-law/derogations/
- https://www.lawinsider.com/dictionary/concession-request
- https://quollnet.com/article/ncr-meaning-construction
- https://www.levelset.com/blog/what-are-transmittals-in-construction/
- https://www.buildtwin.com/blog/drawing-transmittals-construction-document-delivery/
- https://www.datumnotes.com/resources/blog/why-architecture-projects-lose-decisions
- https://www.projectmanagertemplate.com/post/decision-logs-the-ultimate-guide
- https://adr.github.io/
- https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
- https://www.theengineeringdesign.com/blog/mep-clash-detection-bim
- https://helonic.com/blog/mep-coordination-best-practices
- https://gdiengdesign.com/mep-systems-podium-high-rise-buildings/
- https://www.natlmep.com/how-mep-systems-affect-every-building-decision-with-architectural-teams/
- https://ams-wa.com/fire-safety-facade-regulations/
- https://www.rebuildcostassessment.com/technical-insight/cladding-and-high-risk-buildings-rebuild-assessment-misconceptions
- https://www.testfit.io/feasibility-tools/parking-ratio-calculator
- https://www.ths-concepts.co.uk/guide-to-nia-gia-measurements/
- https://www.zepth.com/minutes-of-meeting-construction-accountability/
- https://www.autodesk.com/blogs/construction/construction-meetings/