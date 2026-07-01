"""Trace foundation spine — the never-delete, bi-temporal decision store.

Build-order step 1 from docs/02-architecture.md §9. No LLM / network / API key:
this is the pure data layer every later Trace feature sits on. Supersession
invalidates (closes valid_to, links superseded_by) but never deletes, which is
both the correct memory design and the golden-thread/QP audit requirement.
"""
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


def get_valid_decisions(conn: sqlite3.Connection) -> list[Decision]:
    rows = conn.execute(
        "SELECT * FROM decisions WHERE valid_to IS NULL AND status = 'valid' ORDER BY recorded_at"
    ).fetchall()
    return [_row_to_decision(r) for r in rows]


def get_all_decisions(conn: sqlite3.Connection) -> list[Decision]:
    rows = conn.execute("SELECT * FROM decisions ORDER BY recorded_at, id").fetchall()
    return [_row_to_decision(r) for r in rows]


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


def get_history(conn: sqlite3.Connection, decision_id: str) -> list[Decision]:
    chain: list[Decision] = []
    current = get_decision(conn, decision_id)
    while current is not None:
        chain.append(current)
        current = get_decision(conn, current.superseded_by) if current.superseded_by else None
    return chain
