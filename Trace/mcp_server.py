"""Trace MCP server — the deterministic half of Trace, spoken over the Model
Context Protocol.

`mcp_tools.py` exposes capture/recall as Qwen-Agent tools (LLM-driven, needs the
API key); its docstring flagged a real MCP server as roadmap. This is that
server, and it is deliberately the *certain* half: every tool here is
deterministic and needs **no API key and no network** — it reads the bi-temporal
store, runs the fire-code rule-pack, walks supersession chains, verifies the
SHA-256 audit chain, and returns persisted court verdicts. The LLM does
judgment and language; this server ships facts, proofs and guarantees, so any
MCP client (Claude Desktop, a Qwen agent, an IDE) can ground itself on Trace's
record without trusting a model for the parts that must be certain.

Built on the official `mcp` SDK (FastMCP), stdio transport.

Run it directly:
    python mcp_server.py

Register it with an MCP client, e.g. claude_desktop_config.json:
    {
      "mcpServers": {
        "trace": { "command": "python", "args": ["/abs/path/to/Trace/mcp_server.py"] }
      }
    }

The tool functions below are plain, importable, and dependency-light (no `mcp`
needed to call them) — build_server() is what wraps them as MCP tools.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import rulepack
import store
from court import get_court_records
from scenarios import PROJECTS, open_store

# The second Singapore code-authority pack (BCA Periodic Façade Inspection) —
# proof that rule-packs are pluggable per authority, same engine.
_BCA_RULES = Path(rulepack.__file__).with_name("rules") / "sg-bca"

# One connection per project, cached — to the PERSISTENT store
# (kb/<project>/trace.db), the same file the vault watcher and the bubble
# write/read, so every MCP answer reflects the shared record, not a private
# in-memory copy. Seeded with the demo scenario on first open.
_STORES: dict = {}


def _store(project: str):
    if project not in PROJECTS:
        raise KeyError(project)
    if project not in _STORES:
        _STORES[project] = open_store(project)
    return _STORES[project]


def _dec(d) -> dict:
    return {
        "id": d.id, "status": d.status, "statement": d.statement,
        "discipline": d.discipline, "importance": d.importance,
        "rationale": d.rationale, "assumptions": d.assumptions, "author": d.author,
        "valid_from": d.valid_from, "valid_to": d.valid_to,
        "recorded_at": d.recorded_at, "superseded_by": d.superseded_by,
    }


# ── tools ────────────────────────────────────────────────────────────────────

def list_projects() -> list[dict]:
    """List the projects Trace is watching, with each project's decision count.
    Use this first to discover valid `project` keys for the other tools."""
    return [
        {"key": k, "title": v["title"], "blurb": v["blurb"],
         "decisions": len(store.get_all_decisions(_store(k)))}
        for k, v in PROJECTS.items()
    ]


_STATUSES = ("valid", "proposed", "rejected", "superseded")


def list_decisions(project: str, status: Optional[str] = None) -> dict:
    """Every decision on record for a project (never-delete: superseded and
    rejected decisions are included, not erased). Optionally filter by status
    ('valid', 'proposed', 'rejected', or 'superseded'). Returns id, statement,
    rationale, assumptions, author, and both validity clocks."""
    try:
        conn = _store(project)
    except KeyError:
        return {"error": f"unknown project '{project}'; call list_projects"}
    if status and status not in _STATUSES:
        return {"error": f"unknown status '{status}'; one of {list(_STATUSES)}"}
    ds = store.get_all_decisions(conn)
    if status:
        ds = [d for d in ds if d.status == status]
    return {"project": project, "count": len(ds), "decisions": [_dec(d) for d in ds]}


def get_decision(project: str, decision_id: str) -> dict:
    """One decision in full, plus its supersession history — the chain of what
    replaced it (or what it replaced), each link preserved. `decision_id` is
    project-coded, e.g. '408213-D-001' (the prefix names the project, so a
    cross-project mixup is a detectable error, not a silently wrong record)."""
    try:
        conn = _store(project)
    except KeyError:
        return {"error": f"unknown project '{project}'; call list_projects"}
    d = store.get_decision(conn, decision_id)
    if d is None:
        return {"error": f"no decision '{decision_id}' in {project}"}
    return {"project": project, "decision": _dec(d),
            "history": [_dec(h) for h in store.get_history(conn, decision_id)]}


def decisions_asof(project: str, as_of: str) -> dict:
    """Bi-temporal time-travel: the decisions that were BOTH on record and valid
    as of a past instant — 'what did you know, and when'. A supersession recorded
    later never rewrites the past. `as_of` is an ISO-8601 timestamp, e.g.
    '2026-02-01' or '2026-02-01T00:00:00Z'."""
    try:
        conn = _store(project)
    except KeyError:
        return {"error": f"unknown project '{project}'; call list_projects"}
    try:
        valid = store.get_valid_asof(conn, as_of)
    except (ValueError, TypeError):
        return {"error": f"could not parse as_of '{as_of}'; use ISO-8601 like 2026-02-01"}
    return {"project": project, "as_of": as_of,
            "valid": [_dec(d) for d in valid]}


def check_compliance(
    height_m: Optional[float] = None,
    boundary_distance_m: Optional[float] = None,
    age_years: Optional[float] = None,
    cladding_combustible: Optional[bool] = None,
    cladding_class_0: Optional[bool] = None,
    is_composite: Optional[bool] = None,
    core_class0_or_b: Optional[bool] = None,
    inspection_within_cycle: Optional[bool] = None,
    inspection_competent_person: Optional[bool] = None,
    pack: str = "scdf",
) -> dict:
    """Run a proposed facade/building context against a deterministic Singapore
    rule-pack — the gate that makes Trace's invalidation alert never mis-fire.
    Returns each violation with its rule id, rationale, the clause it cites, the
    downstream blast-radius, and the official source URL. `pack` selects the code
    authority: 'scdf' (SCDF Fire Code 2023) or 'bca' (BCA Periodic Façade
    Inspection) — rule-packs are pluggable per authority."""
    context: dict = {}
    b = {}
    if height_m is not None:
        b["height_m"] = height_m
    if boundary_distance_m is not None:
        b["boundary_distance_m"] = boundary_distance_m
    if age_years is not None:
        b["age_years"] = age_years
    if b:
        context["building"] = b
    facade = {}
    clad = {}
    if cladding_combustible is not None:
        clad["combustible"] = cladding_combustible
    if cladding_class_0 is not None:
        clad["class_0"] = cladding_class_0
    if is_composite is not None:
        clad["is_composite"] = is_composite
    if core_class0_or_b is not None:
        clad["core_class0_or_b"] = core_class0_or_b
    if clad:
        facade["cladding"] = clad
    insp = {}
    if inspection_within_cycle is not None:
        insp["within_cycle"] = inspection_within_cycle
    if inspection_competent_person is not None:
        insp["competent_person"] = inspection_competent_person
    if insp:
        facade["inspection"] = insp
    if facade:
        context["facade"] = facade

    chosen = (pack or "scdf").lower()
    if chosen not in ("scdf", "bca"):
        return {"error": f"unknown pack '{pack}'; one of ['scdf', 'bca']"}
    rules = rulepack.load_rules(_BCA_RULES) if chosen == "bca" else rulepack.load_rules()
    by_id = {r.id: r for r in rules}
    viols = rulepack.check(context, rules)
    return {
        "pack": chosen,
        "context": context,
        "compliant": not viols,
        "violations": [
            {"rule_id": v.rule_id, "rationale": v.rationale, "citation": v.citation,
             "blast_radius": v.blast_radius,
             "provision": getattr(by_id.get(v.rule_id), "provision", ""),
             "url": getattr(by_id.get(v.rule_id), "url", "")}
            for v in viols
        ],
    }


def get_code_provision(query: str = "") -> list[dict]:
    """The code registry: provisions curated from primary sources at authoring
    time (SCDF fire code + BCA façade inspection), each with its official link —
    'automation, not a tool', so the clause comes to you instead of sending you
    to search a statutes portal. Optionally filter by a substring of the
    citation, provision, or rule id."""
    rules = rulepack.load_rules() + rulepack.load_rules(_BCA_RULES)
    out = [{"rule_id": r.id, "citation": r.citation, "provision": r.provision, "url": r.url}
           for r in rules if r.provision or r.url]
    if query:
        q = query.lower()
        out = [e for e in out if q in (e["rule_id"] + e["citation"] + e["provision"]).lower()]
    return out


def verify_audit_chain(project: str) -> dict:
    """Verify the tamper-evident audit chain: recompute the whole SHA-256
    hash-chained audit log for a project. Returns intact=true with the event
    count, or intact=false with the first sequence number whose hash does not
    reconcile (any edit, insert or deletion anywhere breaks every hash after it)."""
    try:
        conn = _store(project)
    except KeyError:
        return {"error": f"unknown project '{project}'; call list_projects"}
    ok, n = store.verify_audit_chain(conn)
    return {"project": project, "intact": ok, "events": n} if ok \
        else {"project": project, "intact": False, "first_bad_seq": n}


def court_records(project: str) -> dict:
    """The persisted decision-court verdicts for a project: for each reviewed
    proposal, the verdict, the decision it broke, the cited clause, and the for/
    against/rationale arguments — the defensible record a liable QP stands behind."""
    try:
        conn = _store(project)
    except KeyError:
        return {"error": f"unknown project '{project}'; call list_projects"}
    return {"project": project, "records": get_court_records(conn)}


TOOLS = [
    list_projects, list_decisions, get_decision, decisions_asof,
    check_compliance, get_code_provision, verify_audit_chain, court_records,
]


def build_server():
    """Wrap the deterministic tools above as an MCP server (FastMCP, stdio).
    Imported lazily so the tool functions stay callable without the mcp package."""
    from mcp.server.fastmcp import FastMCP

    server = FastMCP(
        "trace",
        instructions=(
            "Trace is a design-decision memory agent for construction (AEC). These tools are the "
            "deterministic, no-key half: read the never-delete decision record, time-travel it, "
            "gate a proposal through the fire-code rule-pack, fetch the exact clause + official "
            "link, verify the tamper-evident audit chain, and read persisted court verdicts. Call "
            "list_projects first to get valid project keys."
        ),
    )
    for fn in TOOLS:
        server.tool(name=fn.__name__)(fn)
    return server


if __name__ == "__main__":
    build_server().run()
