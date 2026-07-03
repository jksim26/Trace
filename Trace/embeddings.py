"""Qwen embeddings for hybrid recall — the semantic half of retrieval.

Lexical overlap (strategies.py) is exact but blind to paraphrase: "make the
exterior envelope cheaper" shares no content words with "facade = non-combustible
rainscreen", yet it is the same decision. This module adds a semantic signal via
Qwen's text-embedding-v3 on the Singapore DashScope endpoint (the same OpenAI-
compatible client recall already uses), so recall can blend the two.

It is strictly additive and degradable: it needs the API key, and every caller
wraps its use so that no key / no network / any embedding error falls straight
back to the deterministic lexical path. No embeddings, no behaviour change.
"""
from __future__ import annotations

import math
import os

EMBED_MODEL = os.getenv("TRACE_EMBED_MODEL", "text-embedding-v3")
_BATCH = 10  # DashScope text-embedding batch ceiling


def cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def client_embedder(client, model: str = EMBED_MODEL, batch: int = _BATCH):
    """Build an embedder — texts -> list[vector] — over an OpenAI-compatible
    client (the recall client, pointed at DashScope). Batches so it stays honest
    at scale, and preserves input order via each item's returned index."""
    def embed(texts):
        texts = list(texts)
        out: list = []
        for i in range(0, len(texts), batch):
            resp = client.embeddings.create(model=model, input=texts[i:i + batch])
            out.extend(item.embedding for item in sorted(resp.data, key=lambda d: d.index))
        return out
    return embed
