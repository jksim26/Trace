"""Demo scenarios — three Singapore projects, three companies, three code stories.

This is what gives Trace something to REMEMBER: each project store carries
currently-valid decisions, rejected proposals (preserved, never deleted),
superseded chains (bi-temporal — time-travel works on them), and persisted
court records. Every rejection is a REAL state transition on the record
(status 'rejected' via the court), never just prose.

  • tanglin-rise  — SG residential high-rise; the SCDF fire rule-pack gates
                    invalidation (the deterministic story, as in the video)
  • kranji-hub    — SG industrial/MEP; invalidation hinges on the LLM
                    premise check over stored assumptions (no rule involved)
  • pearl-vista   — SG residential tower past its 20th year; a DIFFERENT
                    Singapore authority's pack (rules/sg-bca/, the Periodic
                    Façade Inspection regime) — rule-packs are pluggable per
                    code authority (SCDF, BCA, …)

Every project has a six-digit code; decision ids are minted as
'<code>-D-<nnn>', so an id names its project wherever it is cited — across the
bubble's one-brain chat, MCP clients, and court records.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import rulepack
from capture import Captured
from court import Verdict, _persist
from kb import KB_ROOT
from store import (
    Decision, add_decision, connect, init_db, reject_decision,
    set_project_code, supersede_decision,
)

_RULES_DIR = Path(rulepack.__file__).with_name("rules")


def project_rules(project_key: str) -> list:
    """The loaded rule-pack list a project's invalidation checks run against —
    the SCDF fire pack for every building, plus each extra pack the project's
    registry entry names (e.g. pearl-vista adds the BCA PFI pack)."""
    rules = rulepack.load_rules()
    for pack in PROJECTS[project_key].get("packs", []):
        rules += rulepack.load_rules(_RULES_DIR / pack)
    return rules


def _record_court(conn, proposal_id: str, breaks_id: str, citation: str,
                  for_arg: str, against_arg: str, rationale: str,
                  rejected_at: str) -> None:
    """Seed a court REJECT the way the live court applies one: the verdict is
    persisted first (the chain shows the ruling before the transition it
    authorizes), then the proposal's fate lands on its row (proposed -> rejected)."""
    _persist(conn, Captured(Decision(statement="", id=proposal_id)), Verdict(
        conflict=True, verdict="REJECT", breaks=breaks_id, citation=citation,
        for_argument=for_arg, against_argument=against_arg, rationale=rationale),
        created_at=rejected_at)
    reject_decision(conn, proposal_id, rejected_at=rejected_at)


def _tanglin(conn) -> None:
    add_decision(conn, Decision(  # 408213-D-001
        statement="Facade cladding = non-combustible mineral rainscreen (A1 core, Class 0 outer layers)",
        discipline="facade", importance=5,
        rationale="Building is 95 m (> 15 m); SCDF Fire Code 2023 Cl 3.5.1 mandates wholly "
                  "non-combustible external walls.",
        assumptions=["building height remains above 15 m",
                     "combustible external cladding is prohibited over 15 m"],
        author=["K. Lim (design QP / architect)", "M. Ong (fire engineer)"],
        recorded_at="2026-01-14T11:42Z", valid_from="2026-01-14T11:42Z"))
    add_decision(conn, Decision(  # 408213-D-002
        statement="VE proposal: swap facade cladding to polyethylene-core ACP under the 'or equivalent' clause",
        discipline="facade", status="proposed", importance=5,
        rationale="Cost plan over budget; largest single saving on the facade package.",
        assumptions=["PE-core ACP is an acceptable equivalent to the specified rainscreen"],
        author=["T. Chua (main contractor, commercial)"],
        recorded_at="2026-03-03T14:00Z", valid_from="2026-03-03T14:00Z"))
    add_decision(conn, Decision(  # 408213-D-003
        statement="Wet riser + residential sprinkler provision to SCDF Fire Code Ch 6 throughout the tower",
        discipline="fire", importance=5,
        rationale="Mandatory for a 95 m residential building; sized with the facade strategy in mind.",
        assumptions=["building remains residential (Purpose Group II)"],
        author=["M. Ong (fire engineer)"],
        recorded_at="2026-01-20T10:00Z", valid_from="2026-01-20T10:00Z"))
    add_decision(conn, Decision(  # 408213-D-004 — will be superseded by D-006
        statement="Sky-terrace balustrade = laminated glass, 1.1 m",
        discipline="architecture", importance=3,
        rationale="Client preference for unobstructed views at the level-20 sky terrace.",
        assumptions=["wind-tunnel study confirms glass panel pressures at level 20"],
        author=["K. Lim (design QP / architect)"],
        recorded_at="2026-01-28T15:00Z", valid_from="2026-01-28T15:00Z"))
    add_decision(conn, Decision(  # 408213-D-005
        statement="Facade access by roof BMU (building maintenance unit); no abseiling on the street elevations",
        discipline="structural", importance=4,
        rationale="Periodic Facade Inspection regime requires safe close-range access; BMU rails "
                  "coordinated with the roof plant layout.",
        assumptions=["roof dead-load reserve accommodates BMU rails"],
        author=["S. Raj (structural)"],
        recorded_at="2026-02-05T09:30Z", valid_from="2026-02-05T09:30Z"))
    supersede_decision(conn, "408213-D-004", Decision(  # 408213-D-006 supersedes D-004
        statement="Sky-terrace balustrade = aluminium vertical-fin, 1.1 m (glass dropped)",
        discipline="architecture", importance=3,
        rationale="Wind-tunnel results exceeded the glass panel pressure limits at level 20 — "
                  "the premise of the glass option failed.",
        assumptions=["fin spacing satisfies BCA climbability guidance"],
        author=["K. Lim (design QP / architect)"],
        recorded_at="2026-02-20T14:00Z", valid_from="2026-02-20T14:00Z"),
        superseded_at="2026-02-20T14:00Z")
    _record_court(
        conn, "408213-D-002", "408213-D-001", "SCDF Fire Code 2023 Cl 3.5.1",
        "The PE-core ACP is visually identical, covered by the 'or equivalent' clause, and the "
        "largest single saving on the facade package.",
        "A polyethylene core is combustible; it cannot be an 'equivalent' under Cl 3.5.1 for a "
        "95 m building and falsifies 408213-D-001's recorded premise.",
        "Substitution rejected. However material the saving, a PE-core panel cannot satisfy "
        "Cl 3.5.1; adopting it would falsify the premise of 408213-D-001 and expose the named QP "
        "to personal liability under Building Control Act s.9.",
        rejected_at="2026-03-03T15:00Z")


def _kranji(conn) -> None:
    add_decision(conn, Decision(  # 517294-D-001
        statement="Chiller plant = 2 × 350 RT air-cooled, electrical demand held within the 400 kVA site supply",
        discipline="mep", importance=5,
        rationale="SP Group confirmed 400 kVA as the committed supply for phase 1; plant sized to fit it.",
        assumptions=["site power budget is 400 kVA",
                     "no process cooling load beyond comfort cooling in phase 1"],
        author=["D. Tan (mechanical lead, Meridian M&E)"],
        recorded_at="2026-02-10T09:00Z", valid_from="2026-02-10T09:00Z"))
    add_decision(conn, Decision(  # 517294-D-002
        statement="Rooftop PV array 180 kWp to offset landlord services load",
        discipline="mep", importance=3,
        rationale="Green Mark points and tenant ESG requirements; export not required.",
        assumptions=["roof dead-load reserve of 25 kg/m² is available for panels and ballast"],
        author=["A. Wong (electrical, Meridian M&E)"],
        recorded_at="2026-02-18T11:00Z", valid_from="2026-02-18T11:00Z"))
    add_decision(conn, Decision(  # 517294-D-003 — rejected proposal (LLM premise check story)
        statement="Tenant fit-out proposal: add a 900 m² cold room (process cooling) in phase 1",
        discipline="mep", status="proposed", importance=4,
        rationale="Anchor tenant requirement — caught by Trace's LLM premise check "
                  "(no fire rule involved): process cooling breaks the premise that phase-1 "
                  "load is comfort-cooling only within the 400 kVA supply.",
        assumptions=["existing supply can absorb the cold-room load"],
        author=["ColdStore Logistics Pte Ltd (tenant)"],
        recorded_at="2026-04-02T16:00Z", valid_from="2026-04-02T16:00Z"))
    add_decision(conn, Decision(  # 517294-D-004 — will be superseded by D-005
        statement="Main switchboard located in basement 1 plant room",
        discipline="mep", importance=4,
        rationale="Shortest cable runs to the substation.",
        assumptions=["basement 1 is outside the site's flood-prone envelope"],
        author=["A. Wong (electrical, Meridian M&E)"],
        recorded_at="2026-02-12T10:00Z", valid_from="2026-02-12T10:00Z"))
    supersede_decision(conn, "517294-D-004", Decision(  # 517294-D-005 supersedes D-004
        statement="Main switchboard relocated to ground floor, 600 mm above platform level",
        discipline="mep", importance=4,
        rationale="PUB flood-risk review placed basement 1 inside the flood-prone envelope — "
                  "the premise of the basement location failed.",
        assumptions=["ground-floor plant room retains 1-hr fire separation"],
        author=["A. Wong (electrical, Meridian M&E)"],
        recorded_at="2026-03-15T09:00Z", valid_from="2026-03-15T09:00Z"),
        superseded_at="2026-03-15T09:00Z")
    _record_court(
        conn, "517294-D-003", "517294-D-001", "LLM premise check (Qwen)",
        "The anchor tenant requires a 900 m² cold room in phase 1 and will not sign without it.",
        "Process cooling directly falsifies 517294-D-001's stated premises: the 400 kVA budget "
        "and 'no process cooling load in phase 1'. The chiller plant and supply were sized on them.",
        "Proposal rejected as submitted. It cannot proceed until the supply upgrade is committed "
        "or the load is rescheduled to phase 2 — otherwise 517294-D-001's basis of design is "
        "falsified.",
        rejected_at="2026-04-02T17:00Z")


def _pearl(conn) -> None:
    add_decision(conn, Decision(  # 629481-D-001
        statement="PFI programme committed: full façade inspection by the appointed Competent Person, "
                  "7-year cycle, all elevations (visual survey + close-range where indicated)",
        discipline="facade", importance=5,
        rationale="Pearl Vista is 78 m and 27 years old — the Periodic Façade Inspection regime "
                  "(in force 1 Jan 2022) applies: taller than 13 m and over 20 years old, every 7 years.",
        assumptions=["the building remains above 13 m and over 20 years old",
                     "a Competent Person is appointed for every inspection cycle"],
        author=["H. Nair (Competent Person, façade engineer)", "L. Goh (MCST council chair)"],
        recorded_at="2026-01-12T10:00Z", valid_from="2026-01-12T10:00Z"))
    add_decision(conn, Decision(  # 629481-D-002 — rejected proposal (BCA rule-pack story)
        statement="Managing-agent proposal: skip the Competent Person appointment this cycle and rely "
                  "on the maintenance contractor's drone footage alone",
        discipline="facade", status="proposed", importance=5,
        rationale="Sinking-fund pressure; the drone survey is already paid for under the "
                  "maintenance contract.",
        assumptions=["contractor drone footage alone is an acceptable substitute for a Competent "
                     "Person's inspection"],
        author=["Pinnacle Managing Agents Pte Ltd"],
        recorded_at="2026-03-10T14:30Z", valid_from="2026-03-10T14:30Z"))
    add_decision(conn, Decision(  # 629481-D-003
        statement="North-elevation repair: hack back delaminated render, replace corroded brackets "
                  "with stainless-steel fixings",
        discipline="facade", importance=4,
        rationale="The close-range survey found render spalling and bracket corrosion on the "
                  "north elevation.",
        assumptions=["repair scope covers every defect flagged in the 2026 close-range survey"],
        author=["H. Nair (Competent Person, façade engineer)"],
        recorded_at="2026-02-14T09:00Z", valid_from="2026-02-14T09:00Z"))
    add_decision(conn, Decision(  # 629481-D-004 — will be superseded by D-005
        statement="Interim measure: safety netting over the north-elevation footpath until repairs complete",
        discipline="facade", importance=4,
        rationale="Loose render found above a public walkway; interim protection required while "
                  "the repair funding is approved.",
        assumptions=["netting remains a stopgap until the permanent repair is completed"],
        author=["H. Nair (Competent Person, façade engineer)", "L. Goh (MCST council chair)"],
        recorded_at="2026-02-14T09:30Z", valid_from="2026-02-14T09:30Z"))
    supersede_decision(conn, "629481-D-004", Decision(  # 629481-D-005 supersedes D-004
        statement="North-elevation permanent repair completed and verified; safety netting removed",
        discipline="facade", importance=4,
        rationale="The repair closed out the defect list — the interim-measure premise no "
                  "longer holds.",
        assumptions=["close-out verified by the Competent Person"],
        author=["H. Nair (Competent Person, façade engineer)"],
        recorded_at="2026-05-08T11:00Z", valid_from="2026-05-08T11:00Z"),
        superseded_at="2026-05-08T11:00Z")
    _record_court(
        conn, "629481-D-002", "629481-D-001",
        "Building Control Act — Periodic Façade Inspection (in force 1 Jan 2022)",
        "The contractor's drone survey is already paid for and covers every elevation in 4K.",
        "Drone footage alone is not a façade inspection: the PFI duty requires an appointed "
        "Competent Person, and skipping the appointment falsifies 629481-D-001's recorded premise.",
        "Proposal rejected. An unsupervised visual-only survey does not discharge the owner's "
        "PFI duty for a 78 m, 27-year-old building; the Competent Person appointment stands "
        "as committed in 629481-D-001.",
        rejected_at="2026-03-10T15:30Z")


PROJECTS = {
    "tanglin-rise": {
        "title": "Tanglin Rise · 95 m residential · Singapore",
        "code": "408213",
        "context": {"building": {"height_m": 95, "boundary_distance_m": 7.5}},
        "blurb": "Project: Tanglin Rise — a 28-storey, 95 m residential condominium in Singapore "
                 "(Lim & Ong Architects). Code regime: SCDF Fire Code 2023 (rule-pack Cl 3.5.1 / "
                 "3.5.4 / 3.15.13); the design QP carries personal criminal liability under "
                 "Building Control Act s.9. Invalidation here is gated by the deterministic "
                 "fire rule-pack.",
        "build": _tanglin,
    },
    "kranji-hub": {
        "title": "Kranji Logistics Hub · industrial MEP · Singapore",
        "code": "517294",
        "context": {"building": {"height_m": 12, "boundary_distance_m": 30}},
        "blurb": "Project: Kranji Logistics Hub — a two-storey logistics facility in Singapore "
                 "(Meridian M&E Consultants). Power and cooling decisions hinge on a committed "
                 "400 kVA supply; invalidation here is caught by Trace's LLM premise check over "
                 "stored assumptions — no rule-pack involved.",
        "build": _kranji,
    },
    "pearl-vista": {
        "title": "Pearl Vista · 78 m residential (1999) · Singapore",
        "code": "629481",
        "packs": ["sg-bca"],  # a SECOND code authority's pack gates this project's invalidation
        "context": {"building": {"height_m": 78, "age_years": 27, "boundary_distance_m": 12}},
        "blurb": "Project: Pearl Vista — a 24-storey, 78 m residential tower in Singapore, "
                 "completed 1999 (Veritas Façade Consultants for the MCST). Past its 20th year, "
                 "the Periodic Façade Inspection regime applies: taller than 13 m, every 7 years, "
                 "by an appointed Competent Person. Invalidation here is gated by a SECOND "
                 "Singapore authority's rule-pack (rules/sg-bca/) — the packs are pluggable per "
                 "code authority.",
        "build": _pearl,
    },
}


def build_store(project_key: str):
    """A fresh, fully-seeded IN-MEMORY store — the deterministic demo fixture
    tests build against. Live surfaces (bubble, MCP server, vault watcher)
    share the persistent on-disk store instead: open_store()."""
    conn = connect(":memory:")
    init_db(conn)
    # The code must be pinned BEFORE the first write: ids are minted from it and
    # are immutable once on the audit chain.
    set_project_code(conn, PROJECTS[project_key]["code"])
    PROJECTS[project_key]["build"](conn)
    return conn


def open_store(project_key: str, root: Optional[Path] = None):
    """Open the project's PERSISTENT store — kb/<project>/trace.db, next to the
    inbox it feeds. Every surface (bubble chat, MCP server, vault watcher)
    opens this one file, so a note ingested by the watcher is immediately
    visible to the chat and to MCP clients, and nothing is lost on restart.

    Seeded with the demo scenario on first open — built in a temp file and
    atomically renamed into place, so a crash mid-seed never leaves a
    half-seeded store behind. `root` (or $TRACE_DB_DIR) overrides the kb/
    location, e.g. for tests. Raises KeyError for an unknown project."""
    meta = PROJECTS[project_key]
    root = Path(root) if root else Path(os.environ.get("TRACE_DB_DIR") or KB_ROOT)
    db = root / project_key / "trace.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    if not db.exists() or db.stat().st_size == 0:
        seed = db.with_name(f"trace.seed-{os.getpid()}.db")
        conn = connect(str(seed))
        init_db(conn)
        set_project_code(conn, meta["code"])
        meta["build"](conn)
        conn.close()  # checkpoints WAL, so the rename moves the complete store
        os.replace(seed, db)
    return connect(str(db))
