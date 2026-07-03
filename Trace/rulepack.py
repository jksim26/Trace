"""Deterministic AEC rule-pack — the certain half of check_invalidation.

Loads YAML rules (Trace/rules/*.yaml) and checks a structured decision context
against them. A rule fires a Violation when ALL its `when` conditions hold AND
any `require` condition fails. This is what makes the demo's invalidation alert
never mis-fire; the LLM premise check (needs the API key) is the general half.
See docs/02-architecture.md §6.
"""
from __future__ import annotations

import operator
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_RULES_DIR = Path(__file__).with_name("rules")

_OPS = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "gte": operator.ge,
    "lt": operator.lt,
    "lte": operator.le,
    "in": lambda v, s: v in s,
    "not_in": lambda v, s: v not in s,
}


@dataclass
class Rule:
    id: str
    when: dict = field(default_factory=dict)
    require: dict = field(default_factory=dict)
    rationale: str = ""
    citation: str = ""
    blast_radius: list = field(default_factory=list)
    provision: str = ""   # the requirement wording, curated from the primary source
    url: str = ""         # official source link — the clause comes to the user


@dataclass
class Violation:
    rule_id: str
    rationale: str = ""
    citation: str = ""
    blast_radius: list = field(default_factory=list)


def load_rules(path=None) -> list[Rule]:
    base = Path(path) if path else _RULES_DIR
    files = [base] if base.is_file() else sorted(base.glob("*.yaml"))
    rules: list[Rule] = []
    for f in files:
        for raw in yaml.safe_load(f.read_text(encoding="utf-8")) or []:
            rules.append(
                Rule(
                    id=raw["id"],
                    when=raw.get("when", {}),
                    require=raw.get("require", {}),
                    rationale=raw.get("rationale", ""),
                    citation=raw.get("citation", ""),
                    blast_radius=raw.get("blast_radius", []),
                    provision=raw.get("provision", ""),
                    url=raw.get("url", ""),
                )
            )
    return rules


def _get(context, dotted: str):
    cur = context
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _match(value, condition: dict) -> bool:
    return all(_OPS[op](value, target) for op, target in condition.items())


def _applies(rule: Rule, context) -> bool:
    for path, cond in rule.when.items():
        value = _get(context, path)
        if value is None or not _match(value, cond):
            return False
    return True


def _satisfied(rule: Rule, context) -> bool:
    for path, cond in rule.require.items():
        value = _get(context, path)
        if value is None:
            continue  # attribute not set by this decision -> rule not engaged on it
        if not _match(value, cond):
            return False
    return True


def check(context, rules: list[Rule]) -> list[Violation]:
    return [
        Violation(r.id, r.rationale, r.citation, r.blast_radius)
        for r in rules
        if _applies(r, context) and not _satisfied(r, context)
    ]
