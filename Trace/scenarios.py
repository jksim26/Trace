"""Demo scenarios — three projects, three companies, three code regimes.

This is what gives Trace something to REMEMBER: each project store carries
currently-valid decisions, rejected proposals (preserved, never deleted),
superseded chains (bi-temporal — time-travel works on them), and persisted
court records.

  • tanglin-rise    — SG residential high-rise; SCDF fire rule-pack gates
                      invalidation (the deterministic story, as in the video)
  • kranji-hub      — SG industrial/MEP; invalidation hinges on the LLM
                      premise check over stored assumptions (no fire rule)
  • maple-wharf     — UK residential; a DIFFERENT rule-pack (rules/uk/) —
                      the codes are pluggable per jurisdiction
"""
from __future__ import annotations

from capture import Captured
from court import Verdict, _persist
from store import Decision, add_decision, connect, init_db, supersede_decision


def _record_court(conn, proposal_id: str, breaks_id: str, citation: str,
                  for_arg: str, against_arg: str, rationale: str) -> None:
    _persist(conn, Captured(Decision(statement="", id=proposal_id)), Verdict(
        conflict=True, verdict="REJECT", breaks=breaks_id, citation=citation,
        for_argument=for_arg, against_argument=against_arg, rationale=rationale))


def _tanglin(conn) -> None:
    add_decision(conn, Decision(  # D-001
        statement="Facade cladding = non-combustible mineral rainscreen (A1 core, Class 0 outer layers)",
        discipline="facade", importance=5,
        rationale="Building is 95 m (> 15 m); SCDF Fire Code 2023 Cl 3.5.1 mandates wholly "
                  "non-combustible external walls.",
        assumptions=["building height remains above 15 m",
                     "combustible external cladding is prohibited over 15 m"],
        author=["K. Lim (design QP / architect)", "M. Ong (fire engineer)"],
        recorded_at="2026-01-14T11:42Z", valid_from="2026-01-14T11:42Z"))
    add_decision(conn, Decision(  # D-002
        statement="VE proposal: swap facade cladding to polyethylene-core ACP under the 'or equivalent' clause",
        discipline="facade", status="rejected", importance=5,
        rationale="Cost plan over budget; largest single saving on the facade package. "
                  "REJECTED by the decision court: a PE core is combustible — breaches Cl 3.5.1.",
        assumptions=["PE-core ACP is an acceptable equivalent to the specified rainscreen"],
        author=["T. Chua (main contractor, commercial)"],
        recorded_at="2026-03-03T14:00Z", valid_from="2026-03-03T14:00Z"))
    add_decision(conn, Decision(  # D-003
        statement="Wet riser + residential sprinkler provision to SCDF Fire Code Ch 6 throughout the tower",
        discipline="fire", importance=5,
        rationale="Mandatory for a 95 m residential building; sized with the facade strategy in mind.",
        assumptions=["building remains residential (Purpose Group II)"],
        author=["M. Ong (fire engineer)"],
        recorded_at="2026-01-20T10:00Z", valid_from="2026-01-20T10:00Z"))
    add_decision(conn, Decision(  # D-004 — will be superseded by D-005
        statement="Sky-terrace balustrade = laminated glass, 1.1 m",
        discipline="architecture", importance=3,
        rationale="Client preference for unobstructed views at the level-20 sky terrace.",
        assumptions=["wind-tunnel study confirms glass panel pressures at level 20"],
        author=["K. Lim (design QP / architect)"],
        recorded_at="2026-01-28T15:00Z", valid_from="2026-01-28T15:00Z"))
    add_decision(conn, Decision(  # D-005
        statement="Facade access by roof BMU (building maintenance unit); no abseiling on the street elevations",
        discipline="structural", importance=4,
        rationale="Periodic Facade Inspection regime requires safe close-range access; BMU rails "
                  "coordinated with the roof plant layout.",
        assumptions=["roof dead-load reserve accommodates BMU rails"],
        author=["S. Raj (structural)"],
        recorded_at="2026-02-05T09:30Z", valid_from="2026-02-05T09:30Z"))
    supersede_decision(conn, "D-004", Decision(  # D-006 supersedes D-004
        statement="Sky-terrace balustrade = aluminium vertical-fin, 1.1 m (glass dropped)",
        discipline="architecture", importance=3,
        rationale="Wind-tunnel results exceeded the glass panel pressure limits at level 20 — "
                  "the premise of the glass option failed.",
        assumptions=["fin spacing satisfies BCA climbability guidance"],
        author=["K. Lim (design QP / architect)"],
        recorded_at="2026-02-20T14:00Z", valid_from="2026-02-20T14:00Z"),
        superseded_at="2026-02-20T14:00Z")
    _record_court(
        conn, "D-002", "D-001", "SCDF Fire Code 2023 Cl 3.5.1",
        "The PE-core ACP is visually identical, covered by the 'or equivalent' clause, and the "
        "largest single saving on the facade package.",
        "A polyethylene core is combustible; it cannot be an 'equivalent' under Cl 3.5.1 for a "
        "95 m building and falsifies D-001's recorded premise.",
        "Substitution rejected. However material the saving, a PE-core panel cannot satisfy "
        "Cl 3.5.1; adopting it would falsify the premise of D-001 and expose the named QP to "
        "personal liability under Building Control Act s.9.")


def _kranji(conn) -> None:
    add_decision(conn, Decision(  # D-001
        statement="Chiller plant = 2 × 350 RT air-cooled, electrical demand held within the 400 kVA site supply",
        discipline="mep", importance=5,
        rationale="SP Group confirmed 400 kVA as the committed supply for phase 1; plant sized to fit it.",
        assumptions=["site power budget is 400 kVA",
                     "no process cooling load beyond comfort cooling in phase 1"],
        author=["D. Tan (mechanical lead, Meridian M&E)"],
        recorded_at="2026-02-10T09:00Z", valid_from="2026-02-10T09:00Z"))
    add_decision(conn, Decision(  # D-002
        statement="Rooftop PV array 180 kWp to offset landlord services load",
        discipline="mep", importance=3,
        rationale="Green Mark points and tenant ESG requirements; export not required.",
        assumptions=["roof dead-load reserve of 25 kg/m² is available for panels and ballast"],
        author=["A. Wong (electrical, Meridian M&E)"],
        recorded_at="2026-02-18T11:00Z", valid_from="2026-02-18T11:00Z"))
    add_decision(conn, Decision(  # D-003 — rejected proposal (LLM premise check story)
        statement="Tenant fit-out proposal: add a 900 m² cold room (process cooling) in phase 1",
        discipline="mep", status="rejected", importance=4,
        rationale="Anchor tenant requirement. REJECTED as proposed: process cooling breaks the "
                  "premise that phase-1 load is comfort-cooling only within the 400 kVA supply — "
                  "caught by Trace's LLM premise check (no fire rule involved).",
        assumptions=["existing supply can absorb the cold-room load"],
        author=["ColdStore Logistics Pte Ltd (tenant)"],
        recorded_at="2026-04-02T16:00Z", valid_from="2026-04-02T16:00Z"))
    add_decision(conn, Decision(  # D-004 — will be superseded by D-005
        statement="Main switchboard located in basement 1 plant room",
        discipline="mep", importance=4,
        rationale="Shortest cable runs to the substation.",
        assumptions=["basement 1 is outside the site's flood-prone envelope"],
        author=["A. Wong (electrical, Meridian M&E)"],
        recorded_at="2026-02-12T10:00Z", valid_from="2026-02-12T10:00Z"))
    supersede_decision(conn, "D-004", Decision(  # D-005 supersedes D-004
        statement="Main switchboard relocated to ground floor, 600 mm above platform level",
        discipline="mep", importance=4,
        rationale="PUB flood-risk review placed basement 1 inside the flood-prone envelope — "
                  "the premise of the basement location failed.",
        assumptions=["ground-floor plant room retains 1-hr fire separation"],
        author=["A. Wong (electrical, Meridian M&E)"],
        recorded_at="2026-03-15T09:00Z", valid_from="2026-03-15T09:00Z"),
        superseded_at="2026-03-15T09:00Z")
    _record_court(
        conn, "D-003", "D-001", "LLM premise check (Qwen)",
        "The anchor tenant requires a 900 m² cold room in phase 1 and will not sign without it.",
        "Process cooling directly falsifies D-001's stated premises: the 400 kVA budget and "
        "'no process cooling load in phase 1'. The chiller plant and supply were sized on them.",
        "Proposal rejected as submitted. It cannot proceed until the supply upgrade is committed "
        "or the load is rescheduled to phase 2 — otherwise D-001's basis of design is falsified.")


def _maple(conn) -> None:
    add_decision(conn, Decision(  # D-001
        statement="Facade = terracotta rainscreen on A2-s1,d0 mineral wool insulation",
        discipline="facade", importance=5,
        rationale="The tower is 62 m (a relevant building over 18 m): combustible external wall "
                  "materials are banned — Building Regulations reg 7(2). Recorded for the golden thread.",
        assumptions=["building remains a relevant building (over 18 m)",
                     "combustible external cladding is banned over 18 m"],
        author=["R. Wells (architect, Harwood & Partner)", "P. Desai (fire)"],
        recorded_at="2026-01-09T10:00Z", valid_from="2026-01-09T10:00Z"))
    add_decision(conn, Decision(  # D-002
        statement="VE proposal: ACM panels with polyethylene core on the east elevation",
        discipline="facade", status="rejected", importance=5,
        rationale="Cost saving proposed by the facade subcontractor. REJECTED: PE-core ACM is "
                  "combustible — banned over 18 m by reg 7(2); would also fail Gateway 2 review.",
        assumptions=["ACM-PE is acceptable as a like-for-like alternative"],
        author=["FaceTech Cladding Ltd (subcontractor)"],
        recorded_at="2026-02-25T14:30Z", valid_from="2026-02-25T14:30Z"))
    add_decision(conn, Decision(  # D-003 — will be superseded by D-005
        statement="Single-stair core with enhanced smoke control",
        discipline="architecture", importance=5,
        rationale="Plan efficiency at concept stage.",
        assumptions=["single-stair remains acceptable for a residential building of this height"],
        author=["R. Wells (architect, Harwood & Partner)"],
        recorded_at="2026-01-16T09:00Z", valid_from="2026-01-16T09:00Z"))
    add_decision(conn, Decision(  # D-004
        statement="Golden-thread record kept in the CDE with immutable versioning; Trace holds the decision layer",
        discipline="client", importance=4,
        rationale="BSA 2022 golden-thread duty for a higher-risk building; Gateway submissions "
                  "must evidence the basis of safety decisions.",
        assumptions=["the building is classified as a higher-risk building (HRB)"],
        author=["J. Mokoena (client-side PM)"],
        recorded_at="2026-01-23T11:00Z", valid_from="2026-01-23T11:00Z"))
    supersede_decision(conn, "D-003", Decision(  # D-005 supersedes D-003
        statement="Two-staircase core adopted",
        discipline="architecture", importance=5,
        rationale="Policy shift: new residential buildings over 18 m require a second staircase — "
                  "the single-stair premise no longer holds.",
        assumptions=["core re-plan absorbed within the current GIA"],
        author=["R. Wells (architect, Harwood & Partner)", "P. Desai (fire)"],
        recorded_at="2026-03-20T10:00Z", valid_from="2026-03-20T10:00Z"),
        superseded_at="2026-03-20T10:00Z")
    _record_court(
        conn, "D-002", "D-001", "Building Regulations 2010 reg 7(2)",
        "The subcontractor offers ACM at a material saving on the east elevation package.",
        "PE-core ACM is combustible and banned on a 62 m residential building; the proposal "
        "falsifies D-001's recorded premise and would fail Gateway 2.",
        "Substitution rejected. Reg 7(2) leaves no discretion for a relevant building over 18 m; "
        "the golden-thread record of this refusal is retained for the Gateway submission.")


PROJECTS = {
    "tanglin-rise": {
        "title": "Tanglin Rise · 95 m residential · Singapore",
        "blurb": "Project: Tanglin Rise — a 28-storey, 95 m residential condominium in Singapore "
                 "(Lim & Ong Architects). Code regime: SCDF Fire Code 2023 (rule-pack Cl 3.5.1 / "
                 "3.5.4 / 3.15.13); the design QP carries personal criminal liability under "
                 "Building Control Act s.9. Invalidation here is gated by the deterministic "
                 "fire rule-pack.",
        "build": _tanglin,
    },
    "kranji-hub": {
        "title": "Kranji Logistics Hub · industrial MEP · Singapore",
        "blurb": "Project: Kranji Logistics Hub — a two-storey logistics facility in Singapore "
                 "(Meridian M&E Consultants). Power and cooling decisions hinge on a committed "
                 "400 kVA supply; invalidation here is caught by Trace's LLM premise check over "
                 "stored assumptions — no fire rule involved.",
        "build": _kranji,
    },
    "maple-wharf": {
        "title": "Maple Wharf · 62 m residential · London (UK)",
        "blurb": "Project: Maple Wharf — a 19-storey, 62 m residential tower in London (Harwood & "
                 "Partner Architects). Code regime: England — the combustible-cladding ban over "
                 "18 m (Building Regulations reg 7(2), rule-pack rules/uk/), the BSA 2022 golden "
                 "thread, and the two-staircase policy for tall residential buildings.",
        "build": _maple,
    },
}


def build_store(project_key: str, db_path: str = ":memory:"):
    """Build (or reopen) a project's store. `db_path` defaults to an ephemeral
    in-memory store (what tests and the CLI demo want: a fresh, isolated store
    every call). Pass a real file path to persist a project across restarts —
    the seed data is only written the first time a given file is opened, so
    reopening an existing store never re-inserts the demo decisions or
    clobbers anything a live session added since."""
    conn = connect(db_path)
    init_db(conn)
    is_empty = conn.execute("SELECT 1 FROM decisions LIMIT 1").fetchone() is None
    if is_empty:
        PROJECTS[project_key]["build"](conn)
    return conn
