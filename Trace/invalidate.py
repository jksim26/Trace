"""C2 — check_invalidation: the centrepiece.

Fire an alert the moment a newly-captured decision breaks a live premise.
Two halves:
  1. The deterministic rule-pack gate (so the demo alert never mis-fires).
  2. llm_premise_check — the general half: Qwen reads each prior decision's
     STORED ASSUMPTIONS and judges whether the new decision falsifies one.
     Runs only when the rule-pack is silent and a client is available.

When an alert fires, `breaks` is chosen premise-aware: the prior valid decision
whose stated assumptions the new decision most overlaps, with the specific
broken assumption named (falling back to the latest same-discipline decision).
See docs/02-architecture.md §4 (Pipeline A) / §6.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

from capture import Captured
from rulepack import check, load_rules
from store import Decision, get_valid_decisions

load_dotenv()

MODEL = "qwen-plus"
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

# Every project carries its OWN building context (scenarios.PROJECTS[...]["context"]);
# checks run against the context passed in, never a hardcoded building — a 95 m
# tower's height rules must not fire on a two-storey logistics shed.

# Machine-checkable capture attributes -> rule-context paths.
_ATTR_PATHS = {
    "cladding_combustible": "facade.cladding.combustible",
    "cladding_class_0": "facade.cladding.class_0",
    "cladding_is_composite": "facade.cladding.is_composite",
    "cladding_core_class0_or_b": "facade.cladding.core_class0_or_b",
    "boundary_distance_m": "building.boundary_distance_m",
}

_STOP = {
    "the", "a", "an", "and", "or", "to", "of", "for", "on", "in", "at", "it",
    "this", "that", "is", "are", "was", "were", "be", "been", "with", "as", "by",
}


@dataclass
class Alert:
    new: Decision
    rule_id: str
    rationale: str
    citation: str
    blast_radius: list = field(default_factory=list)
    breaks: Optional[Decision] = None
    broken_premise: Optional[str] = None  # the specific stored assumption broken
    source: str = "rule"                  # "rule" | "llm"


def _words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2 and w not in _STOP}


def _new_decision_words(captured: Captured) -> set:
    return _words(
        f"{captured.decision.statement} {captured.decision.rationale} "
        + " ".join(str(k) for k in captured.attributes)
    )


def _rule_context(captured: Captured, context: Optional[dict] = None) -> dict:
    ctx = {"building": dict((context or {}).get("building", {}))}
    for key, val in captured.attributes.items():
        path = _ATTR_PATHS.get(key)
        if path is None or val is None:
            continue
        cur = ctx
        parts = path.split(".")
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = val
    return ctx


def _pick_breaks(conn, captured: Captured) -> tuple[Optional[Decision], Optional[str]]:
    """Premise-aware, deterministic: the prior valid decision whose stated
    assumptions the new decision most overlaps, naming the specific assumption.
    Falls back to the latest valid decision in the same discipline."""
    new_words = _new_decision_words(captured)
    best: tuple[int, Optional[Decision], Optional[str]] = (0, None, None)
    for d in get_valid_decisions(conn):
        for assumption in d.assumptions:
            score = len(new_words & _words(assumption))
            if score > best[0]:
                best = (score, d, assumption)
    if best[1] is not None:
        return best[1], best[2]
    same_discipline = [
        d for d in get_valid_decisions(conn)
        if d.discipline == captured.decision.discipline
    ]
    return (same_discipline[-1] if same_discipline else None), None


def check_invalidation(conn, captured: Captured, rules=None, client=None,
                       model: str = MODEL, context: Optional[dict] = None) -> list[Alert]:
    """Rule-pack first (deterministic, gates the demo). If the rules are silent
    and a client is provided, fall back to the general LLM premise check.
    `context` is the PROJECT's building context (e.g. height, boundary distance)
    — pass the right project's, never another building's."""
    rules = rules if rules is not None else load_rules()
    violations = check(_rule_context(captured, context), rules)
    if violations:
        breaks, premise = _pick_breaks(conn, captured)
        return [
            Alert(captured.decision, v.rule_id, v.rationale, v.citation,
                  v.blast_radius, breaks, premise, source="rule")
            for v in violations
        ]
    if client is not None:
        return llm_premise_check(conn, captured, client=client, model=model)
    return []


_PREMISE_SYS = (
    "You are Trace's premise checker for AEC design decisions. You get one NEW "
    "decision and one PRIOR decision with its stated assumptions. Judge ONLY from "
    "the text given whether the new decision falsifies any stated assumption "
    "(premise) of the prior decision. Reply with strict JSON, nothing else: "
    '{"breaks": true|false, "premise": "<the broken assumption, verbatim, or empty>", '
    '"why": "<one sentence>"}'
)


def _parse_premise_json(text: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        out = json.loads(cleaned)
        return out if isinstance(out, dict) else {}
    except json.JSONDecodeError:
        return {}


def llm_premise_check(conn, captured: Captured, client=None, model: str = MODEL,
                      max_candidates: int = 5) -> list[Alert]:
    """The general half of invalidation: for each candidate prior decision
    (narrowed deterministically by keyword overlap with its stored assumptions,
    to bound cost), ask Qwen whether the new decision breaks a stated premise."""
    new_words = _new_decision_words(captured)
    scored = []
    for d in get_valid_decisions(conn):
        if not d.assumptions:
            continue
        score = len(new_words & _words(d.statement + " " + " ".join(d.assumptions)))
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: -x[0])
    candidates = [d for _, d in scored[:max_candidates]]
    if not candidates:
        return []

    if client is None:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)

    alerts: list[Alert] = []
    for d in candidates:
        case = (
            f"NEW DECISION: {captured.decision.statement}\n"
            f"NEW RATIONALE: {captured.decision.rationale or '(none stated)'}\n"
            f"NEW ATTRIBUTES: {json.dumps(captured.attributes) or '{}'}\n\n"
            f"PRIOR DECISION {d.id}: {d.statement}\n"
            "PRIOR ASSUMPTIONS:\n"
            + "\n".join(f"  {i + 1}. {a}" for i, a in enumerate(d.assumptions))
        )
        resp = client.chat.completions.create(
            model=model, temperature=0,
            messages=[{"role": "system", "content": _PREMISE_SYS},
                      {"role": "user", "content": case}],
        )
        verdict = _parse_premise_json(resp.choices[0].message.content)
        if verdict.get("breaks") is True:
            alerts.append(Alert(
                captured.decision,
                rule_id="LLM-PREMISE",
                rationale=verdict.get("why", "A stated premise is falsified."),
                citation="LLM premise check (Qwen)",
                blast_radius=[],
                breaks=d,
                broken_premise=verdict.get("premise") or None,
                source="llm",
            ))
    return alerts


def render_alert(alert: Alert) -> str:
    lines = ["⚠  TRACE INVALIDATION ALERT", "━" * 44]
    lines.append(f"NEW:    {alert.new.statement}")
    if alert.breaks is not None:
        lines.append(f"BREAKS: {alert.breaks.id} — {alert.breaks.statement}")
        if alert.broken_premise:
            lines.append(f'        premise broken: "{alert.broken_premise}"')
        elif alert.breaks.rationale:
            lines.append(f"        premise: {alert.breaks.rationale}")
    lines.append(f"WHY:    {alert.rationale}  [{alert.citation}]")
    if alert.blast_radius:
        lines.append("BLAST RADIUS: " + ", ".join(alert.blast_radius))
    return "\n".join(lines)
