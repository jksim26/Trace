"""Trace demo CLI — runs the four "Tanglin Rise" scenes for the camera (C6),
plus the staged ambient card (C7).

Scene 1 capture -> Scene 2 invalidation alert + court -> Scene 3 recall +
abstention -> Scene 4 bi-temporal time-travel. Real Qwen calls happen for
capture (x2), the court (x3), and the recall answer; the alert, abstention, and
time-travel are deterministic.

Run from the Trace/ dir:
  python cli.py            live Qwen calls (needs DASHSCOPE_API_KEY)
  python cli.py --offline  replay canned Qwen responses (no key, no network)
  python cli.py --record   live calls AND refresh the offline fixture from them
  (add --pause to step through scene by scene)
"""
from __future__ import annotations

import sys
from pathlib import Path

from audit import render_chain_status
from capture import capture_decision
from court import convene, render_verdict
from invalidate import check_invalidation, render_alert
from recall import recall_decisions
from store import add_decision, connect, get_all_decisions, get_valid_asof, init_db

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    _console = Console()
    RICH = True
except Exception:  # rich not installed -> plain text still films fine
    RICH = False

TRANSCRIPTS = Path(__file__).resolve().parent.parent / "demo" / "transcripts"

# A deliberately tight "critical-context" budget so the meter visibly bites in the
# demo — the whole point of retrieve-to-budget is injecting only what matters.
DEMO_BUDGET = 600


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


def _budget_bar(used: int, budget: int, width: int = 24) -> str:
    filled = min(width, round(width * used / budget)) if budget else 0
    return "█" * filled + "░" * (width - filled) + f"   {used} / {budget} tokens"


_STATUS = {"valid": "IN FORCE", "proposed": "PROPOSED", "rejected": "REJECTED",
           "superseded": "SUPERSEDED"}

# Tanglin Rise building context (95 m, ~7.5 m to boundary): the rule-pack checks
# THIS project's facts — Cl 3.5.1's height limb applies, its boundary limb doesn't.
PROJECT_CONTEXT = {"building": {"height_m": 95, "boundary_distance_m": 7.5}}


def _trail(conn) -> str:
    lines = ["Nothing is deleted — every version stays on the record:", ""]
    for d in get_all_decisions(conn):
        if d.status == "proposed":
            when = f"proposed {(d.valid_from or '')[:10]} · pending the court"
        elif d.status == "rejected":
            when = f"proposed {(d.valid_from or '')[:10]} · rejected by the court"
        elif d.valid_to:
            when = f"{(d.valid_from or '')[:10]} → {d.valid_to[:10]}  (superseded)"
        else:
            when = f"{(d.valid_from or '')[:10]} → current"
        lines.append(f"  {d.id}  [{_STATUS.get(d.status, d.status)}]   {when}")
        lines.append(f"        {d.statement}")
        if d.superseded_by:
            lines.append(f"        superseded_by → {d.superseded_by}")
    return "\n".join(lines)


def ambient_card(conn) -> str:
    everything = get_all_decisions(conn)
    valid = [d for d in everything if d.status == "valid"]
    pending = [d for d in everything if d.status == "proposed"]
    rejected = [d for d in everything if d.status == "rejected"]
    return (
        f"2nd-storey facade  ·  {len(everything)} decision(s) on record\n"
        f"  • {len(valid)} currently valid\n"
        f"  • {len(pending)} pending proposal(s) · {len(rejected)} rejected\n"
        f"  • live constraint: D-001 non-combustible facade (> 15 m, SCDF Cl 3.5)"
    )


def _asof(conn, as_of: str) -> str:
    ds = get_valid_asof(conn, as_of)
    body = ", ".join(f"{d.id} {d.statement[:44]}" for d in ds) if ds else "(nothing on record yet)"
    return f"as of {as_of[:10]}:  {body}"


def run(pause: bool = False, client=None):
    conn = connect(":memory:")
    init_db(conn)

    _rule("SCENE 1 - CAPTURE  (Concept Design, 14 Jan 2026)")
    t1 = (TRANSCRIPTS / "01-concept-design-2026-01-14.md").read_text(encoding="utf-8")
    for c in capture_decision(t1, source_episode="transcript-2026-01-14",
                              recorded_at="2026-01-14T11:42Z", valid_from="2026-01-14T11:42Z",
                              client=client):
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
                              recorded_at="2026-03-03T14:00Z", valid_from="2026-03-03T14:00Z",
                              client=client):
        alerts = check_invalidation(conn, c, context=PROJECT_CONTEXT)
        c.decision.status = "proposed"
        add_decision(conn, c.decision)  # never delete — the proposal stays on the record
        for a in alerts:
            _panel(render_alert(a), title="!! INVALIDATION ALERT", style="red")
        if alerts:
            # The court's verdict is a real state transition: REJECT marks the
            # proposal `rejected` on the record; ALLOW would adopt it instead.
            _panel(render_verdict(convene(conn, c, client=client, context=PROJECT_CONTEXT)),
                   title="The decision court — 3 Qwen roles deliberate", style="red")
        _panel(_trail(conn) + "\n\n" + render_chain_status(conn),
               title="Never-delete trail (C4) — tamper-evident", style="yellow")
    _pause(pause)

    _rule("SCENE 3 - RECALL UNDER BUDGET  (Handover, 12 May 2026)")
    for q in [
        "Why the non-combustible facade cladding, and can we still change it?",
        "Did we ever decide the sky-terrace planter or balustrade material?",
    ]:
        r = recall_decisions(conn, q, budget=DEMO_BUDGET, client=client)
        cited = ("cited: " + ", ".join(r.cited)) if r.cited else "cited: (none — abstained)"
        selected = f"scanned {r.candidates} relevant decision(s) → packed {len(r.cited)} within budget"
        _panel(
            f"Q: {q}\n\nA: {r.answer}\n\n{cited}\n{selected}\nbudget  {_budget_bar(r.used, r.budget)}",
            title="Recall", style=("blue" if r.abstained else "magenta"),
        )
    _pause(pause)

    _rule("SCENE 4 - TIME-TRAVEL  (bi-temporal memory)")
    _panel(
        "Rewind Trace's memory to any date — reconstruct what was valid and known:\n\n"
        f"  {_asof(conn, '2026-01-01T00:00Z')}\n"
        f"  {_asof(conn, '2026-02-01T00:00Z')}\n"
        f"  {_asof(conn, '2026-03-03T14:00Z')}\n\n"
        "When the ACM swap was floated on 3 Mar, D-001's non-combustible premise was already\n"
        "valid — the QP was on notice. 'What did you know, and when' is what s.9 liability turns on.",
        title="Bi-temporal time-travel", style="cyan",
    )
    _pause(pause)

    _rule("AMBIENT (staged) - 'you opened the 2nd-storey facade drawing'")
    _panel(ambient_card(conn), title="Trace", style="cyan")
    return conn


if __name__ == "__main__":
    _client = None
    if "--offline" in sys.argv:
        from replay import ReplayClient
        _client = ReplayClient()
        _panel("OFFLINE REPLAY — canned Qwen responses from demo_replay.json.\n"
               "No API key or network needed. Run without --offline for live calls;\n"
               "run --record (with a key) to refresh the fixture from real output.",
               title="offline mode", style="yellow")
    elif "--record" in sys.argv:
        from capture import _client as _real_client
        from replay import RecordingClient
        _client = RecordingClient(_real_client())
        _panel("RECORDING — live Qwen calls, refreshing demo_replay.json as they stream.",
               title="record mode", style="yellow")
    run(pause="--pause" in sys.argv, client=_client)
