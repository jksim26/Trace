# Trace Foundation Spine — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the never-delete, bi-temporal decision store — the data layer every later Trace feature sits on — with passing tests, using no LLM/API calls.

**Architecture:** A single SQLite table `decisions` holds each design decision as a row with bi-temporal validity (`valid_from`/`valid_to`, `recorded_at`/`superseded_at`) and a `superseded_by` self-link. Supersession never deletes: it closes the old row's `valid_to`, stamps `superseded_at`, sets `status='superseded'`, and links `superseded_by` to the new row. A thin `store.py` module exposes add / get / list-valid / supersede / walk-history. This is build-order step 1 from `docs/02-architecture.md` §9 and satisfies the data half of success criteria C1 (capture) and C4 (immutable trail).

**Tech Stack:** Python 3, stdlib `sqlite3` + `dataclasses` + `json` (no third-party runtime deps), `pytest` for tests. Flat module layout under `Trace/` (matches the existing `Trace/test_connection.py` convention).

**Scope:** Data layer only — **no Qwen, no network, no API key needed.** The LLM phases (capture, invalidation, recall, MCP wrap, demo) are separate plans, gated on `DASHSCOPE_API_KEY` (see Roadmap at the end and `docs/09-manual-requirements.md` §A).

---

## File Structure

- Create: `Trace/schema.sql` — the `decisions` table DDL (single source of truth for the schema).
- Create: `Trace/store.py` — the `Decision` dataclass + store functions (`connect`, `init_db`, `add_decision`, `get_decision`, `get_valid_decisions`, `supersede_decision`, `get_history`).
- Create: `Trace/test_store.py` — pytest tests for the store.
- Modify: `Trace/requirements.txt` (currently empty) — add `openai`, `python-dotenv` (used by the existing `test_connection.py`), `pytest`.

Tests run from inside `Trace/` (`cd Trace && python -m pytest`), so `from store import ...` resolves and `schema.sql` is found next to `store.py`.

---

### Task 1: Project deps + schema + `init_db`

**Files:**
- Modify: `Trace/requirements.txt`
- Create: `Trace/schema.sql`
- Create: `Trace/store.py`
- Test: `Trace/test_store.py`

- [ ] **Step 1: Populate `Trace/requirements.txt`**

```
openai>=1.0
python-dotenv>=1.0
pytest>=8.0
```

- [ ] **Step 2: Write `Trace/schema.sql`**

```sql
CREATE TABLE IF NOT EXISTS decisions (
    id             TEXT PRIMARY KEY,
    statement      TEXT NOT NULL,
    discipline     TEXT,
    riba_stage     INTEGER,
    author         TEXT,                 -- JSON array of strings
    rationale      TEXT,
    assumptions    TEXT,                 -- JSON array of strings
    brief_ref      TEXT,
    importance     INTEGER,
    valid_from     TEXT,                 -- when true in the world
    valid_to       TEXT,                 -- NULL = currently valid
    recorded_at    TEXT,                 -- when the system learned it
    superseded_at  TEXT,
    superseded_by  TEXT REFERENCES decisions(id),
    status         TEXT NOT NULL DEFAULT 'valid'
                       CHECK (status IN ('valid','superseded','proposed')),
    source_episode TEXT
);
```

- [ ] **Step 3: Write the failing test for `init_db`**

```python
# Trace/test_store.py
from store import connect, init_db


def _fresh():
    conn = connect(":memory:")
    init_db(conn)
    return conn


def test_init_creates_decisions_table():
    conn = _fresh()
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='decisions'"
    ).fetchone()
    assert row is not None
```

- [ ] **Step 4: Run it and verify it fails**

Run: `cd Trace && python -m pytest test_store.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'store'`.

- [ ] **Step 5: Write `connect` + `init_db` in `Trace/store.py`**

```python
# Trace/store.py
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(db_path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(_SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
```

- [ ] **Step 6: Run it and verify it passes**

Run: `cd Trace && python -m pytest test_store.py -q`
Expected: PASS (1 passed).

- [ ] **Step 7: Commit**

```bash
git add Trace/requirements.txt Trace/schema.sql Trace/store.py Trace/test_store.py
git commit -m "feat(spine): SQLite schema + init_db"
```

---

### Task 2: `Decision` dataclass + `add_decision` / `get_decision` round-trip

**Files:**
- Modify: `Trace/store.py`
- Test: `Trace/test_store.py`

- [ ] **Step 1: Write the failing tests**

```python
# append to Trace/test_store.py
from store import Decision, add_decision, get_decision


def test_round_trip_preserves_fields():
    conn = _fresh()
    d = Decision(
        statement="Facade = terracotta on A2 mineral wool",
        discipline="facade",
        author=["R. Wells", "P. Desai"],
        assumptions=["building remains an HRB (>18m)"],
        importance=5,
        recorded_at="2026-01-14T11:45Z",
    )
    add_decision(conn, d)
    got = get_decision(conn, d.id)
    assert got.statement == "Facade = terracotta on A2 mineral wool"
    assert got.author == ["R. Wells", "P. Desai"]          # JSON round-trips to list
    assert got.assumptions == ["building remains an HRB (>18m)"]
    assert got.status == "valid"
    assert got.valid_to is None
    assert got.valid_from == "2026-01-14T11:45Z"           # defaults to recorded_at


def test_auto_id_sequence():
    conn = _fresh()
    a = add_decision(conn, Decision(statement="A"))
    b = add_decision(conn, Decision(statement="B"))
    assert a.id == "D-001"
    assert b.id == "D-002"


def test_get_missing_returns_none():
    conn = _fresh()
    assert get_decision(conn, "D-999") is None
```

- [ ] **Step 2: Run and verify failure**

Run: `cd Trace && python -m pytest test_store.py -q`
Expected: FAIL — `ImportError: cannot import name 'Decision'`.

- [ ] **Step 3: Implement the dataclass + add/get in `Trace/store.py`**

```python
# append to Trace/store.py
@dataclass
class Decision:
    statement: str
    discipline: str = ""
    riba_stage: Optional[int] = None
    author: list[str] = field(default_factory=list)
    rationale: str = ""
    assumptions: list[str] = field(default_factory=list)
    brief_ref: str = ""
    importance: int = 3
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    recorded_at: Optional[str] = None
    superseded_at: Optional[str] = None
    superseded_by: Optional[str] = None
    status: str = "valid"
    source_episode: str = ""
    id: Optional[str] = None


def _next_id(conn: sqlite3.Connection) -> str:
    n = conn.execute("SELECT COUNT(*) AS n FROM decisions").fetchone()["n"]
    return f"D-{n + 1:03d}"


def _row_to_decision(row: sqlite3.Row) -> Decision:
    return Decision(
        id=row["id"],
        statement=row["statement"],
        discipline=row["discipline"],
        riba_stage=row["riba_stage"],
        author=json.loads(row["author"] or "[]"),
        rationale=row["rationale"],
        assumptions=json.loads(row["assumptions"] or "[]"),
        brief_ref=row["brief_ref"],
        importance=row["importance"],
        valid_from=row["valid_from"],
        valid_to=row["valid_to"],
        recorded_at=row["recorded_at"],
        superseded_at=row["superseded_at"],
        superseded_by=row["superseded_by"],
        status=row["status"],
        source_episode=row["source_episode"],
    )


def add_decision(conn: sqlite3.Connection, decision: Decision) -> Decision:
    if decision.id is None:
        decision.id = _next_id(conn)
    if decision.recorded_at is None:
        decision.recorded_at = _now()
    if decision.valid_from is None:
        decision.valid_from = decision.recorded_at
    conn.execute(
        """INSERT INTO decisions
             (id, statement, discipline, riba_stage, author, rationale, assumptions,
              brief_ref, importance, valid_from, valid_to, recorded_at, superseded_at,
              superseded_by, status, source_episode)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            decision.id, decision.statement, decision.discipline, decision.riba_stage,
            json.dumps(decision.author), decision.rationale, json.dumps(decision.assumptions),
            decision.brief_ref, decision.importance, decision.valid_from, decision.valid_to,
            decision.recorded_at, decision.superseded_at, decision.superseded_by,
            decision.status, decision.source_episode,
        ),
    )
    conn.commit()
    return decision


def get_decision(conn: sqlite3.Connection, decision_id: str) -> Optional[Decision]:
    row = conn.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,)).fetchone()
    return _row_to_decision(row) if row else None
```

- [ ] **Step 4: Run and verify pass**

Run: `cd Trace && python -m pytest test_store.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add Trace/store.py Trace/test_store.py
git commit -m "feat(spine): Decision model + add/get round-trip"
```

---

### Task 3: `get_valid_decisions` (the forgetting filter)

**Files:**
- Modify: `Trace/store.py`
- Test: `Trace/test_store.py`

- [ ] **Step 1: Write the failing test**

```python
# append to Trace/test_store.py
from store import get_valid_decisions


def test_get_valid_lists_only_currently_valid():
    conn = _fresh()
    add_decision(conn, Decision(statement="A", recorded_at="2026-01-01T00:00Z"))
    add_decision(conn, Decision(statement="B", recorded_at="2026-01-02T00:00Z"))
    valid = get_valid_decisions(conn)
    assert [d.statement for d in valid] == ["A", "B"]
```

- [ ] **Step 2: Run and verify failure**

Run: `cd Trace && python -m pytest test_store.py::test_get_valid_lists_only_currently_valid -q`
Expected: FAIL — `ImportError: cannot import name 'get_valid_decisions'`.

- [ ] **Step 3: Implement in `Trace/store.py`**

```python
# append to Trace/store.py
def get_valid_decisions(conn: sqlite3.Connection) -> list[Decision]:
    rows = conn.execute(
        "SELECT * FROM decisions WHERE valid_to IS NULL ORDER BY recorded_at"
    ).fetchall()
    return [_row_to_decision(r) for r in rows]
```

- [ ] **Step 4: Run and verify pass**

Run: `cd Trace && python -m pytest test_store.py -q`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add Trace/store.py Trace/test_store.py
git commit -m "feat(spine): get_valid_decisions filter"
```

---

### Task 4: `supersede_decision` — invalidate, never delete

**Files:**
- Modify: `Trace/store.py`
- Test: `Trace/test_store.py`

- [ ] **Step 1: Write the failing tests**

```python
# append to Trace/test_store.py
import pytest
from store import supersede_decision


def test_supersede_preserves_old_row():
    conn = _fresh()
    add_decision(conn, Decision(statement="terracotta", recorded_at="2026-01-01T00:00Z"))
    new = supersede_decision(
        conn,
        "D-001",
        Decision(statement="ACM cladding", valid_from="2026-03-01T00:00Z"),
        superseded_at="2026-03-01T00:05Z",
    )
    old = get_decision(conn, "D-001")
    assert old is not None                       # NEVER deleted
    assert old.status == "superseded"
    assert old.superseded_by == "D-002"
    assert old.valid_to == "2026-03-01T00:00Z"   # = new.valid_from
    assert old.superseded_at == "2026-03-01T00:05Z"
    assert new.id == "D-002" and new.status == "valid" and new.valid_to is None


def test_supersede_removes_old_from_valid_set():
    conn = _fresh()
    add_decision(conn, Decision(statement="terracotta", recorded_at="2026-01-01T00:00Z"))
    supersede_decision(conn, "D-001", Decision(statement="ACM", valid_from="2026-03-01T00:00Z"))
    assert [d.id for d in get_valid_decisions(conn)] == ["D-002"]


def test_supersede_unknown_id_raises():
    conn = _fresh()
    with pytest.raises(ValueError):
        supersede_decision(conn, "D-404", Decision(statement="x"))
```

- [ ] **Step 2: Run and verify failure**

Run: `cd Trace && python -m pytest test_store.py -q`
Expected: FAIL — `ImportError: cannot import name 'supersede_decision'`.

- [ ] **Step 3: Implement in `Trace/store.py`**

```python
# append to Trace/store.py
def supersede_decision(
    conn: sqlite3.Connection,
    old_id: str,
    new_decision: Decision,
    superseded_at: Optional[str] = None,
) -> Decision:
    old = get_decision(conn, old_id)
    if old is None:
        raise ValueError(f"No decision {old_id} to supersede")
    new = add_decision(conn, new_decision)           # insert the replacement first
    conn.execute(
        """UPDATE decisions
              SET valid_to = ?, superseded_at = ?, superseded_by = ?, status = 'superseded'
            WHERE id = ?""",
        (new.valid_from, superseded_at or _now(), new.id, old_id),
    )
    conn.commit()
    return new
```

- [ ] **Step 4: Run and verify pass**

Run: `cd Trace && python -m pytest test_store.py -q`
Expected: PASS (8 passed).

- [ ] **Step 5: Commit**

```bash
git add Trace/store.py Trace/test_store.py
git commit -m "feat(spine): supersede_decision (never delete)"
```

---

### Task 5: `get_history` — walk the supersession chain (C4)

**Files:**
- Modify: `Trace/store.py`
- Test: `Trace/test_store.py`

- [ ] **Step 1: Write the failing test**

```python
# append to Trace/test_store.py
from store import get_history


def test_get_history_walks_full_chain():
    conn = _fresh()
    add_decision(conn, Decision(statement="v1"))
    supersede_decision(conn, "D-001", Decision(statement="v2"))
    supersede_decision(conn, "D-002", Decision(statement="v3"))
    chain = get_history(conn, "D-001")
    assert [d.id for d in chain] == ["D-001", "D-002", "D-003"]
    assert [d.statement for d in chain] == ["v1", "v2", "v3"]
```

- [ ] **Step 2: Run and verify failure**

Run: `cd Trace && python -m pytest test_store.py::test_get_history_walks_full_chain -q`
Expected: FAIL — `ImportError: cannot import name 'get_history'`.

- [ ] **Step 3: Implement in `Trace/store.py`**

```python
# append to Trace/store.py
def get_history(conn: sqlite3.Connection, decision_id: str) -> list[Decision]:
    chain: list[Decision] = []
    current = get_decision(conn, decision_id)
    while current is not None:
        chain.append(current)
        current = get_decision(conn, current.superseded_by) if current.superseded_by else None
    return chain
```

- [ ] **Step 4: Run and verify pass (full suite green)**

Run: `cd Trace && python -m pytest test_store.py -q`
Expected: PASS (9 passed).

- [ ] **Step 5: Commit**

```bash
git add Trace/store.py Trace/test_store.py
git commit -m "feat(spine): get_history walks superseded_by chain"
```

---

## Self-Review

- **Spec coverage:** Spine covers `docs/02` §9 step 1 (schema + store + never-delete supersede) and the data half of C1 (a record round-trips) + C4 (superseded preserved with `superseded_by`, history walkable). C2/C3/C5/C6/C7 are out of scope here by design (LLM-gated) — see Roadmap.
- **Placeholder scan:** none — every step has runnable code/commands and expected output.
- **Type consistency:** `Decision` field names match the schema columns and the SQL `INSERT`/`UPDATE` column lists; function names (`add_decision`, `get_decision`, `get_valid_decisions`, `supersede_decision`, `get_history`, `connect`, `init_db`) are used identically in tasks and tests.

---

## Roadmap — subsequent plans (gated on `DASHSCOPE_API_KEY`)

Each becomes its own plan once the Qwen account + key exist (`docs/09-manual-requirements.md` §A) and `test_connection.py` is green. Written after the key is in, so they can be precise about real Qwen behaviour rather than guessing.

1. **Capture (C1)** — `capture.py`: `capture_decision(transcript)` via qwen3.7-max function-calling → `Decision` rows. Needs key.
2. **Invalidate (C2, the centrepiece)** — `invalidate.py`: deterministic YAML rule-pack + LLM premise check → push alert; on confirm, call `supersede_decision`. Rule-pack is testable without the key; the LLM half needs it.
3. **Recall (C3)** — `recall.py`: hybrid retrieve → composite re-score → retrieve-to-budget + abstention + budget meter. Needs key (embeddings/rerank).
4. **Audit view (C4)** — thin CLI over `get_history` (no key; can be done anytime after the spine).
5. **Qwen-Agent MCP wrap (C5)** — expose the four tools via `@register_tool`. Needs key.
6. **CLI + staged ambient hero moment (C6/C7)** — `rich` CLI for the three scenes + the scripted "open 2nd-storey drawing" context card reading live from the store.

**Jurisdiction note:** the demo storyline migrates from "Maple Wharf" (UK) to "Tanglin Rise" (SG) — confirm `docs/09` §D1 before the transcripts/rule-pack are written.
