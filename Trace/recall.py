"""C3 — recall_decisions: answer from currently-valid decisions, packed to a
token budget, with honest abstention. See docs/02-architecture.md §4 Pipeline B.

Retrieval + abstention are deterministic (keyword overlap on content words), so
the demo behaves the same every take; the final answer is synthesised by
qwen-plus, grounded ONLY in the packed decisions.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from dotenv import load_dotenv
from openai import OpenAI

from store import Decision, get_valid_decisions

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


def _score(d: Decision, qwords: set) -> int:
    dw = _content_words(f"{d.statement} {d.rationale} {' '.join(d.assumptions)}")
    return len(qwords & dw)


def retrieve(conn, question: str, budget: int = TOKEN_BUDGET):
    qwords = _content_words(question)
    scored = sorted(
        ((d, _score(d, qwords)) for d in get_valid_decisions(conn)),
        key=lambda x: -x[1],
    )
    packed, used = [], 0
    for d, s in scored:
        if s <= 0:
            continue
        cost = _est_tokens(f"{d.statement} {d.rationale}")
        if used + cost > budget:
            break
        packed.append(d)
        used += cost
    return packed, used


_ANSWER_SYS = (
    "You are Trace. Answer the question using ONLY the design decisions provided. "
    "Be concise (at most 2 sentences). Cite decision IDs inline like (D-001). "
    'If the decisions do not answer the question, reply exactly: "No decision on record."'
)


def _fmt(d: Decision) -> str:
    return f"{d.id} [{d.status}] {d.statement} | rationale: {d.rationale} | valid_from: {d.valid_from}"


def recall_decisions(conn, question: str, budget: int = TOKEN_BUDGET, client=None, model: str = MODEL) -> RecallResult:
    packed, used = retrieve(conn, question, budget)
    if not packed:
        return RecallResult("No decision on record; not yet decided.", [], used, budget, True)
    client = client or OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)
    context = "\n".join(_fmt(d) for d in packed)
    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": _ANSWER_SYS},
            {"role": "user", "content": f"Decisions:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return RecallResult(resp.choices[0].message.content.strip(), [d.id for d in packed], used, budget, False)
