from store import Decision
from strategies import STRATEGIES, by_composite, by_importance, by_recency, by_relevance


def _d(id, statement="x", rec="2026-01-01", imp=3):
    return Decision(statement=statement, importance=imp, recorded_at=rec, id=id)


def test_by_recency_newest_first():
    ds = [_d("A", rec="2026-01-01"), _d("B", rec="2026-03-01"), _d("C", rec="2026-02-01")]
    assert [d.id for d in by_recency(ds)] == ["B", "C", "A"]


def test_by_importance_highest_first():
    ds = [_d("A", imp=2), _d("B", imp=5), _d("C", imp=3)]
    assert [d.id for d in by_importance(ds)] == ["B", "C", "A"]


def test_by_relevance_filters_and_ranks():
    ds = [_d("A", statement="facade cladding non-combustible"),
          _d("B", statement="core relocation"),
          _d("C", statement="facade rainscreen")]
    out = [d.id for d in by_relevance(ds, "facade cladding")]
    assert out[0] == "A" and "B" not in out


def test_composite_blends_all_three():
    ds = [_d("hi", statement="facade cladding", rec="2026-03-01", imp=5),
          _d("lo", statement="parking", rec="2026-01-01", imp=1)]
    assert by_composite(ds, "facade cladding")[0].id == "hi"


def test_registry_exposes_named_strategies():
    assert set(STRATEGIES) == {"relevance", "recency", "importance", "composite"}
