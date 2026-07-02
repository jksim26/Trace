"""C3 — recall_decisions: answer from currently-valid decisions, packed to a
token budget, with honest abstention. Directly-relevant rejected/superseded
decisions are added as history, so an answer to "can we change it?" can cite what
was already tried and rejected. See docs/02-architecture.md §4 Pipeline B.

Retrieval + abstention are deterministic (keyword overlap on content words); the
final answer is synthesised by qwen-plus, grounded ONLY in the packed decisions.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from dotenv import load_dotenv
from openai import OpenAI

from store import Decision, get_all_decisions, get_valid_decisions

load_dotenv()

MODEL = "qwen-plus"
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
TOKEN_BUDGET = 8000

_STOP = {
    "the", "a", "an", "and", "or", "did", "we", "do", "does", "is", "are", "was",
    "were", "to", "of", "for", "on", "in", "at", "it", "this", "that", "can",
    "could", "should", "would", "still", "why", "what", "which", "how", "ever",
    "our", "us", "be", "been", "with", "as", "by",
}


def _content_words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2 and w not in _STOP}


def _est_tokens(text: str) -> int:
    return max(1, len(text) // 4)


@dataclass
class RecallResult:
    answer: str
    cited: list = field(default_factory=list)
    used: int = 0
    budget: int = TOKEN_BUDGET
    abstained: bool = False
    candidates: int = 0  # how many decisions matched the query (for the budget meter)


def _score(d: Decision, qwords: set) -> int:
    dw = _content_words(f"{d.statement} {d.rationale} {' '.join(d.assumptions)}")
    return len(qwords & dw)


def _pack(decisions, qwords, budget, used):
    scored = sorted(((d, _score(d, qwords)) for d in decisions), key=lambda x: -x[1])
    packed = []
    for d, s in scored:
        if s <= 0:
            continue
        cost = _est_tokens(f"{d.statement} {d.rationale}")
        if used + cost > budget:
            break
        packed.append(d)
        used += cost
    return packed, used


def retrieve(conn, question: str, budget: int = TOKEN_BUDGET):
    return _pack(get_valid_decisions(conn), _content_words(question), budget, 0)


_ANSWER_SYS = (
    "You are Trace. Answer the question using ONLY the design decisions provided. "
    "Decisions marked [valid] are current; decisions marked [proposed] or [superseded] "
    "were considered but are NOT in force. Be concise (at most 2 sentences), and cite "
    "decision IDs inline like (D-001). If asked whether something can change, answer it "
    "directly and name any [proposed]/[superseded] attempt that was already rejected. "
    'If the decisions do not answer the question, reply exactly: "No decision on record."'
)


def _fmt(d: Decision) -> str:
    return f"{d.id} [{d.status}] {d.statement} | rationale: {d.rationale} | valid_from: {d.valid_from}"


def recall_decisions(conn, question: str, budget: int = TOKEN_BUDGET, client=None, model: str = MODEL) -> RecallResult:
    qwords = _content_words(question)
    valid = get_valid_decisions(conn)
    others = [d for d in get_all_decisions(conn) if d.status != "valid"]
    candidates = sum(1 for d in valid + others if _score(d, qwords) > 0)

    packed, used = _pack(valid, qwords, budget, 0)      # currently-valid first
    extra, used = _pack(others, qwords, budget, used)   # then relevant history (rejected/superseded)
    chosen = packed + extra
    if not chosen:
        # Report the real candidate count: abstention can also happen because the
        # budget was too tight to pack a match, and the meter must not hide that.
        return RecallResult("No decision on record; not yet decided.", [], used, budget, True, candidates)

    client = client or OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)
    context = "\n".join(_fmt(d) for d in chosen)
    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": _ANSWER_SYS},
            {"role": "user", "content": f"Decisions:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return RecallResult(resp.choices[0].message.content.strip(), [d.id for d in chosen], used, budget, False, candidates)
