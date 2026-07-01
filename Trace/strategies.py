"""Multi-strategy recall — the decision memory can be recalled several ways:

  • relevance  — semantic/keyword overlap with the query
  • recency    — most-recently recorded first
  • importance — criticality (core/structural/fire = 5; finishes = 2)
  • validity   — time-travel, via store.get_valid_asof (as-of a date)
  • composite  — relevance + recency + importance blended (Generative Agents, Park 2023)

Pure engine code — no LLM, no network — so it lives in the domain-agnostic core.
See docs/superpowers/specs/2026-07-01-temporal-reasoning-engine-design.md.
"""
from __future__ import annotations

import re

_STOP = {
    "the", "a", "an", "and", "or", "to", "of", "for", "on", "in", "at", "it",
    "this", "that", "is", "are", "was", "were", "be", "by", "as", "with",
    "why", "what", "which", "how", "can", "we", "still", "did",
}


def _words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(w) > 2 and w not in _STOP}


def relevance_score(d, qwords: set) -> int:
    dw = _words(f"{d.statement} {d.rationale} {' '.join(d.assumptions)}")
    return len(qwords & dw)


def by_relevance(decisions, query: str):
    qw = _words(query)
    return sorted((d for d in decisions if relevance_score(d, qw) > 0),
                  key=lambda d: -relevance_score(d, qw))


def by_recency(decisions):
    return sorted(decisions, key=lambda d: d.recorded_at or "", reverse=True)


def by_importance(decisions):
    return sorted(decisions, key=lambda d: d.importance or 0, reverse=True)


def by_composite(decisions, query: str):
    """relevance(0/1) + recency(0..1) + importance(0..1), normalised."""
    qw = _words(query)
    by_time = sorted(decisions, key=lambda x: x.recorded_at or "")
    pos = {id(d): i for i, d in enumerate(by_time)}
    span = max(1, len(decisions) - 1)

    def score(d):
        rel = 1.0 if relevance_score(d, qw) > 0 else 0.0
        rec = pos[id(d)] / span
        imp = (d.importance or 0) / 5.0
        return rel + rec + imp

    return sorted(decisions, key=score, reverse=True)


STRATEGIES = {
    "relevance": lambda decisions, query="": by_relevance(decisions, query),
    "recency": lambda decisions, query="": by_recency(decisions),
    "importance": lambda decisions, query="": by_importance(decisions),
    "composite": lambda decisions, query="": by_composite(decisions, query),
}
