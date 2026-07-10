"""C3 — recall_decisions: answer from currently-valid decisions, packed to a
token budget, with honest abstention. Directly-relevant rejected/superseded
decisions are added as history, so an answer to "can we change it?" can cite what
was already tried and rejected. See docs/02-architecture.md §4 Pipeline B.

Retrieval is HYBRID: lexical overlap AND a Qwen-embedding semantic signal both
gate relevance (so a paraphrase with no shared words is still recalled), and the
candidates are packed in a blended relevance + recency + importance order
(strategies.py, à la Generative Agents) until the token budget is spent. The
semantic half is strictly additive and degradable — no key / no network / any
embedding error falls straight back to the deterministic lexical path, so
abstention stays deterministic. The final answer is synthesised by qwen-plus,
grounded ONLY in the packed decisions.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from dotenv import load_dotenv
from openai import OpenAI

from embeddings import client_embedder, cosine
from store import Decision, get_all_decisions, get_valid_decisions
from strategies import by_hybrid, hybrid_relevant

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


def _sem_scores(question: str, decisions, embedder):
    """Semantic cosine of the query against each decision, as {id(d): cosine}.
    Returns None — so callers fall straight back to lexical — when there is no
    embedder, no decisions, or any embedding call fails (no key / no network)."""
    if not embedder or not decisions:
        return None
    try:
        texts = [f"{d.statement}. {d.rationale}" for d in decisions]
        vecs = embedder([question] + texts)
        if not vecs or len(vecs) != len(decisions) + 1:
            return None
        qv = vecs[0]
        return {id(d): cosine(qv, vecs[i + 1]) for i, d in enumerate(decisions)}
    except Exception:
        return None


def _pack(decisions, question, budget, used, sem=None):
    relevant = hybrid_relevant(decisions, question, sem)   # lexical OR semantic gate
    packed = []
    for d in by_hybrid(relevant, question, sem):           # relevance + recency + importance
        cost = _est_tokens(f"{d.statement} {d.rationale}")
        if used + cost > budget:
            break
        packed.append(d)
        used += cost
    return packed, used


def retrieve(conn, question: str, budget: int = TOKEN_BUDGET, sem=None):
    return _pack(get_valid_decisions(conn), question, budget, 0, sem)


_ANSWER_SYS = (
    "You are Trace. Answer the question using ONLY the design decisions provided. "
    "Decisions marked [valid] are current; [rejected] was refused by the decision court, "
    "[superseded] was replaced, and [proposed] is pending — none of those three is in "
    "force. Be concise (at most 2 sentences), and cite decision IDs inline, exactly as "
    "given, like (D-001) or (408213-D-001). "
    "If asked whether something can change, answer it directly and name any [rejected] or "
    "[superseded] attempt that was already tried. "
    'If the decisions do not answer the question, reply exactly: "No decision on record."'
)


def _fmt(d: Decision) -> str:
    return f"{d.id} [{d.status}] {d.statement} | rationale: {d.rationale} | valid_from: {d.valid_from}"


def recall_decisions(conn, question: str, budget: int = TOKEN_BUDGET, client=None,
                     model: str = MODEL, embedder=None) -> RecallResult:
    valid = get_valid_decisions(conn)
    # History = everything not currently in force, keyed by id (not by status:
    # a status-'valid' row whose validity window has closed must still be
    # recallable as history, not invisible to both sets).
    in_force = {d.id for d in valid}
    others = [d for d in get_all_decisions(conn) if d.id not in in_force]

    # Hybrid retrieval: blend lexical overlap with Qwen-embedding cosine. The
    # embedder rides the same client; with no key / no client it stays None and
    # retrieval is exactly the deterministic lexical path.
    if embedder is None and client is not None:
        embedder = client_embedder(client)
    sem = _sem_scores(question, valid + others, embedder)
    candidates = len(hybrid_relevant(valid + others, question, sem))

    packed, used = _pack(valid, question, budget, 0, sem)      # currently-valid first
    extra, used = _pack(others, question, budget, used, sem)   # then relevant history (rejected/superseded)
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
