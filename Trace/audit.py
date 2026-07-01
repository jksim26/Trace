"""Audit / history view (C4) — walk a supersession chain for the camera.

Pure formatting over store.get_history: shows each version, its validity
window, status, and the superseded_by links. No LLM / API key.
"""
from __future__ import annotations

from store import Decision


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
