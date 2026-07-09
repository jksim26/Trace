"""Trace foundation spine — the never-delete, bi-temporal decision store.

Build-order step 1 from docs/02-architecture.md §9. No LLM / network / API key:
this is the pure data layer every later Trace feature sits on. Supersession
invalidates (closes valid_to, links superseded_by) but never deletes, which is
both the correct memory design and the golden-thread/QP audit requirement.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normalize_ts(ts: Optional[str]) -> Optional[str]:
    """Canonicalize an ISO-8601 timestamp to UTC second precision
    ("%Y-%m-%dT%H:%M:%SZ"), so lexicographic comparison in SQL is always
    chronological. Mixed precisions otherwise mis-sort: "T00:00Z" compares
    AFTER "T00:00:00Z" as a string.
    """
    if ts is None:
        return None
    dt = datetime.fromisoformat(ts.strip().replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(db_path: str = ":memory:") -> sqlite3.Connection:
    # check_same_thread=False: the bubble's HTTP server answers one request at
    # a time but may not be the thread that first built the store cache.
    conn = sqlite3.connect(db_path, check_same_thread=False)
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
    resubmits: Optional[str] = None
    id: Optional[str] = None


_GENESIS = "0" * 64


def _append_audit(conn: sqlite3.Connection, event: str, ref: Optional[str], payload: dict) -> None:
    """Append a tamper-evident event: hash covers the previous event's hash, so
    any later edit anywhere in the log breaks every hash after it."""
    row = conn.execute("SELECT hash FROM audit_log ORDER BY seq DESC LIMIT 1").fetchone()
    prev = row["hash"] if row else _GENESIS
    at = _now()
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(f"{prev}|{event}|{ref or ''}|{canonical}|{at}".encode()).hexdigest()
    conn.execute(
        "INSERT INTO audit_log (event, ref, payload, at, prev_hash, hash) VALUES (?,?,?,?,?,?)",
        (event, ref, canonical, at, prev, h),
    )


def verify_audit_chain(conn: sqlite3.Connection) -> tuple[bool, int]:
    """Recompute the whole chain. Returns (True, event_count) if intact,
    (False, first_bad_seq) if any event was altered, inserted, or removed."""
    prev = _GENESIS
    n = 0
    for r in conn.execute("SELECT * FROM audit_log ORDER BY seq").fetchall():
        expected = hashlib.sha256(
            f"{prev}|{r['event']}|{r['ref'] or ''}|{r['payload']}|{r['at']}".encode()
        ).hexdigest()
        if r["prev_hash"] != prev or r["hash"] != expected:
            return False, r["seq"]
        prev = r["hash"]
        n += 1
    return True, n


def _next_id(conn: sqlite3.Connection) -> str:
    # MAX-based, not COUNT-based: COUNT collides with any explicitly-supplied id.
    n = conn.execute(
        "SELECT MAX(CAST(SUBSTR(id, 3) AS INTEGER)) AS n FROM decisions WHERE id LIKE 'D-%'"
    ).fetchone()["n"]
    return f"D-{(n or 0) + 1:03d}"


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
        resubmits=row["resubmits"],
    )


def add_decision(conn: sqlite3.Connection, decision: Decision) -> Decision:
    if decision.id is None:
        decision.id = _next_id(conn)
    decision.recorded_at = _normalize_ts(decision.recorded_at) or _now()
    decision.valid_from = _normalize_ts(decision.valid_from) or decision.recorded_at
    decision.valid_to = _normalize_ts(decision.valid_to)
    decision.superseded_at = _normalize_ts(decision.superseded_at)
    conn.execute(
        """INSERT INTO decisions
             (id, statement, discipline, riba_stage, author, rationale, assumptions,
              brief_ref, importance, valid_from, valid_to, recorded_at, superseded_at,
              superseded_by, status, source_episode, resubmits)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            decision.id, decision.statement, decision.discipline, decision.riba_stage,
            json.dumps(decision.author), decision.rationale, json.dumps(decision.assumptions),
            decision.brief_ref, decision.importance, decision.valid_from, decision.valid_to,
            decision.recorded_at, decision.superseded_at, decision.superseded_by,
            decision.status, decision.source_episode, decision.resubmits,
        ),
    )
    _append_audit(conn, "add", decision.id, {
        "statement": decision.statement, "discipline": decision.discipline,
        "rationale": decision.rationale, "assumptions": decision.assumptions,
        "author": decision.author, "importance": decision.importance,
        "valid_from": decision.valid_from, "recorded_at": decision.recorded_at,
        "status": decision.status, "source_episode": decision.source_episode,
        "resubmits": decision.resubmits,
    })
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


def get_valid_asof(conn: sqlite3.Connection, as_of: str) -> list[Decision]:
    """Bi-temporal time-travel: decisions that were on record AND valid as of `as_of`.

    Knowledge axis: recorded_at <= as_of (the system knew it by then), and any
    supersession only counts once it was itself known (superseded_at <= as_of) —
    a supersession recorded later, even with a backdated valid_from, must not
    erase what the record showed at the time ("what did you know, and when").
    Validity axis: valid_from <= as_of, and once the closure is known,
    valid_to must still cover as_of. Excludes proposals and rejected
    proposals (neither was ever true in the world).
    `as_of` is an ISO-8601 timestamp string.
    """
    as_of = _normalize_ts(as_of)
    rows = conn.execute(
        """SELECT * FROM decisions
              WHERE status NOT IN ('proposed', 'rejected')
                AND recorded_at <= ? AND valid_from <= ?
                AND ( (superseded_at IS NOT NULL AND superseded_at > ?)
                      OR (valid_to IS NULL OR valid_to > ?) )
           ORDER BY recorded_at, id""",
        (as_of, as_of, as_of, as_of),
    ).fetchall()
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
    if old.status == "superseded":
        raise ValueError(
            f"{old_id} is already superseded by {old.superseded_by}; "
            f"supersede {old.superseded_by} instead (no forking the chain)"
        )
    new = add_decision(conn, new_decision)           # insert the replacement first
    when = _normalize_ts(superseded_at) or _now()
    conn.execute(
        """UPDATE decisions
              SET valid_to = ?, superseded_at = ?, superseded_by = ?, status = 'superseded'
            WHERE id = ?""",
        (new.valid_from, when, new.id, old_id),
    )
    _append_audit(conn, "supersede", old_id, {
        "superseded_by": new.id, "valid_to": new.valid_from, "superseded_at": when,
    })
    conn.commit()
    return new


def get_history(conn: sqlite3.Connection, decision_id: str) -> list[Decision]:
    chain: list[Decision] = []
    current = get_decision(conn, decision_id)
    while current is not None:
        chain.append(current)
        current = get_decision(conn, current.superseded_by) if current.superseded_by else None
    return chain


_STATUSES = {"valid", "superseded", "proposed", "rejected"}


def set_status(conn: sqlite3.Connection, decision_id: str, status: str) -> Decision:
    """Resolve a decision to its outcome (e.g. the court's verdict promoting a
    clean proposal to 'valid', or settling a broken one as 'rejected'). Every
    transition is itself an audited event — a status flip is a write, not a
    silent mutation."""
    if status not in _STATUSES:
        raise ValueError(f"unknown status {status!r}; must be one of {sorted(_STATUSES)}")
    d = get_decision(conn, decision_id)
    if d is None:
        raise ValueError(f"No decision {decision_id} to update")
    conn.execute("UPDATE decisions SET status = ? WHERE id = ?", (status, decision_id))
    _append_audit(conn, "status_change", decision_id, {"from": d.status, "to": status})
    conn.commit()
    d.status = status
    return d


def get_resubmission_chain(conn: sqlite3.Connection, decision_id: str) -> list[Decision]:
    """Walk a chain of retries backwards from `decision_id` through `resubmits`
    links (latest attempt first) — so a rejected proposal that comes back with
    new evidence stays traceable to what it's retrying, instead of looking like
    an unrelated fresh proposal."""
    chain: list[Decision] = []
    current = get_decision(conn, decision_id)
    while current is not None:
        chain.append(current)
        current = get_decision(conn, current.resubmits) if current.resubmits else None
    return chain
