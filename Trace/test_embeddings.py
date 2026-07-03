from types import SimpleNamespace

import pytest

from embeddings import client_embedder, cosine


def test_cosine_is_a_safe_similarity():
    assert cosine([1, 0], [1, 0]) == pytest.approx(1.0)
    assert cosine([1, 0], [0, 1]) == pytest.approx(0.0)
    assert cosine([0, 0], [1, 1]) == 0.0           # zero vector never divides by zero


def _embed_client(calls):
    def create(model, input):
        calls.append({"model": model, "n": len(input)})
        # return data OUT OF ORDER, each tagged with its true index, to prove we re-sort
        data = [SimpleNamespace(index=i, embedding=[float(len(t)), 1.0]) for i, t in enumerate(input)]
        return SimpleNamespace(data=list(reversed(data)))
    return SimpleNamespace(embeddings=SimpleNamespace(create=create))


def test_client_embedder_batches_and_preserves_input_order():
    calls = []
    embed = client_embedder(_embed_client(calls), model="text-embedding-v3", batch=2)
    texts = ["a", "bb", "ccc", "dddd", "eeeee"]          # 5 texts, batch 2 -> 3 calls
    vecs = embed(texts)
    assert len(calls) == 3 and all(c["model"] == "text-embedding-v3" for c in calls)
    assert [len(t) for t in texts] == [int(v[0]) for v in vecs]   # order preserved despite reversal
