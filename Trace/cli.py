"""Trace demo CLI — runs the three "Tanglin Rise" scenes for the camera (C6),
plus the staged ambient card (C7).

Scene 1 capture -> Scene 2 invalidation alert -> Scene 3 recall + abstention.
Real Qwen calls happen for capture (x2) and the recall answer; the alert and the
abstention are deterministic. Run from the Trace/ dir:  python cli.py [--pause]
"""
from __future__ import annotations

import sys
from pathlib import Path

from capture import capture_decision
from invalidate import check_invalidation, render_alert
from recall import recall_decisions
from store import add_decision, connect, get_all_decisions, init_db

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    _console = Console()
    RICH = True
except Exception:  # rich not installed -> plain text still films fine
    RICH = False

TRANSCRIPTS = Path(__file__).resolve().parent.parent / "demo" / "transcripts"


def _panel(text: str, title: str = "", style: str = "white") -> None:
    if RICH:
        _console.print(Panel(Text(text), title=title, border_style=style))
    else:
        print(f"\n== {title} ==\n{text}\n")


def _rule(text: str) -> None:
    if RICH:
        _console.rule(f"[bold]{text}")
    else:
        print("\n" + "=" * 66 + f"\n{text}\n" + "=" * 66)


def _pause(on: bool) -> None:
    if on:
        try:
            input("  [enter to continue] ")
        except EOFError:
            pass


def _log(conn) -> str:
    return "\n".join(f"  {d.id} [{d.status}] {d.statement[:58]}" for d in get_all_decisions(conn))


def ambient_card(conn) -> str:
    everything = get_all_decisions(conn)
    valid = [d for d in everything if d.status == "valid"]
    pending = [d for d in everything if d.status == "proposed"]
    return (
        f"2nd-storey facade  ·  {len(everything)} decision(s) on record\n"
        f"  - {len(valid)} currently valid\n"
        f"  - {len(pending)} pending / rejected proposal(s)\n"
        f"  - live constraint: D-001 non-combustible facade (> 15 m, SCDF Cl 3.5)"
    )


def run(pause: bool = False) -> None:
    conn = connect(":memory:")
    init_db(conn)

    _rule("SCENE 1 - CAPTURE  (Concept Design, 14 Jan 2026)")
    t1 = (TRANSCRIPTS / "01-concept-design-2026-01-14.md").read_text(encoding="utf-8")
    for c in capture_decision(t1, source_episode="transcript-2026-01-14",
                              recorded_at="2026-01-14T11:42Z", valid_from="2026-01-14T11:42Z"):
        d = add_decision(conn, c.decision)
        _panel(
            f"{d.id}  {d.statement}\n\n"
            f"WHY:     {d.rationale}\n"
            f"ASSUMES: " + "; ".join(d.assumptions) + "\n"
            f"WHO:     " + ", ".join(d.author) + f"    STATUS: {d.status}",
            title=f"Captured {d.id}", style="green",
        )
    _pause(pause)

    _rule("SCENE 2 - VALUE ENGINEERING  (3 Mar 2026)")
    t2 = (TRANSCRIPTS / "02-value-engineering-2026-03-03.md").read_text(encoding="utf-8")
    for c in capture_decision(t2, source_episode="transcript-2026-03-03",
                              recorded_at="2026-03-03T14:00Z", valid_from="2026-03-03T14:00Z"):
        alerts = check_invalidation(conn, c)
        c.decision.status = "proposed"
        prop = add_decision(conn, c.decision)  # never delete — preserve the rejected proposal
        for a in alerts:
            _panel(render_alert(a), title="!! INVALIDATION ALERT", style="red")
        _panel(
            f"Proposal {prop.id} recorded as [proposed] and preserved — D-001 stays valid.\n\n" + _log(conn),
            title="Immutable trail (never delete)", style="yellow",
        )
    _pause(pause)

    _rule("SCENE 3 - RECALL UNDER BUDGET  (Handover, 12 May 2026)")
    for q in [
        "Why the non-combustible facade cladding, and can we still change it?",
        "Did we ever decide the sky-terrace planter or balustrade material?",
    ]:
        r = recall_decisions(conn, q)
        cited = ("cited: " + ", ".join(r.cited)) if r.cited else "cited: (none - abstained)"
        _panel(
            f"Q: {q}\n\nA: {r.answer}\n\n{cited}\ncontext budget: {r.used} / {r.budget} tokens",
            title="Recall", style=("blue" if r.abstained else "magenta"),
        )
    _pause(pause)

    _rule("AMBIENT (staged) - 'you opened the 2nd-storey facade drawing'")
    _panel(ambient_card(conn), title="Trace", style="cyan")


if __name__ == "__main__":
    run(pause="--pause" in sys.argv)
