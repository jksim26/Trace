"""C2 — check_invalidation: the centrepiece.

Fire an alert the moment a newly-captured decision breaks a live premise. The
gate is the deterministic rule-pack (so the demo alert never mis-fires); the LLM
premise check is the general fallback, added later. When a rule fires, the prior
valid decision in the same discipline is named as the premise being broken.
See docs/02-architecture.md §4 (Pipeline A) / §6.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from capture import Captured
from rulepack import check, load_rules
from store import Decision, get_valid_decisions

# Tanglin Rise project constants (the demo building: 95 m, so SCDF Cl 3.5 applies).
PROJECT_CONTEXT = {"building": {"height_m": 95}}


@dataclass
class Alert:
    new: Decision
    rule_id: str
    rationale: str
    citation: str
    blast_radius: list = field(default_factory=list)
    breaks: Optional[Decision] = None


def _rule_context(captured: Captured) -> dict:
    ctx = {"building": dict(PROJECT_CONTEXT["building"])}
    if "cladding_combustible" in captured.attributes:
        ctx["facade"] = {"cladding": {"combustible": captured.attributes["cladding_combustible"]}}
    return ctx


def check_invalidation(conn, captured: Captured, rules=None) -> list[Alert]:
    rules = rules if rules is not None else load_rules()
    violations = check(_rule_context(captured), rules)
    if not violations:
        return []
    same_discipline = [
        d for d in get_valid_decisions(conn)
        if d.discipline == captured.decision.discipline
    ]
    breaks = same_discipline[-1] if same_discipline else None
    return [
        Alert(captured.decision, v.rule_id, v.rationale, v.citation, v.blast_radius, breaks)
        for v in violations
    ]


def render_alert(alert: Alert) -> str:
    lines = ["⚠  TRACE INVALIDATION ALERT", "━" * 44]
    lines.append(f"NEW:    {alert.new.statement}")
    if alert.breaks is not None:
        lines.append(f"BREAKS: {alert.breaks.id} — {alert.breaks.statement}")
        if alert.breaks.rationale:
            lines.append(f"        premise: {alert.breaks.rationale}")
    lines.append(f"WHY:    {alert.rationale}  [{alert.citation}]")
    if alert.blast_radius:
        lines.append("BLAST RADIUS: " + ", ".join(alert.blast_radius))
    return "\n".join(lines)
