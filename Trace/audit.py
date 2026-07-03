"""Audit / history view (C4) — walk a supersession chain for the camera,
and render the tamper-evidence status of the audit chain.

Pure formatting over store.get_history / store.verify_audit_chain. No LLM.
"""
from __future__ import annotations

from store import Decision, verify_audit_chain


def render_chain_status(conn) -> str:
    ok, n = verify_audit_chain(conn)
    if ok:
        head = conn.execute("SELECT hash FROM audit_log ORDER BY seq DESC LIMIT 1").fetchone()
        short = head["hash"][:12] if head else "genesis"
        return f"⛓  audit chain VERIFIED — {n} event(s), SHA-256 head {short}…"
    return f"⛓  AUDIT CHAIN BROKEN at event #{n} — the record has been altered"


def render_history(chain: list[Decision]) -> str:
    if not chain:
        return "No decision on record."
    lines = [f"Audit trail — {len(chain)} version(s):"]
    for d in chain:
        window = f"{d.valid_from or '?'} → {d.valid_to or '(current)'}"
        lines.append(f"  {d.id}  [{d.status}]  valid {window}")
        lines.append(f"        {d.statement}")
        if d.superseded_by:
            lines.append(f"        superseded_by → {d.superseded_by}")
    return "\n".join(lines)
