"""The vault watcher — the second brain's intake, wired to the full pipeline.

Polls kb/<project>/inbox/ (the same poll-and-dedupe shape watcher.py uses on
window titles, but on files): drop a markdown meeting note into the inbox and
Trace, unprompted, (1) stores it verbatim as an immutable, audit-chained
EPISODE, (2) captures each decision in it with rationale + assumptions (Qwen
function-calling), (3) checks every capture against the project's rule-pack
and the LLM premise check, (4) convenes the decision court on a conflict —
the verdict lands on the record as a real state transition — and (5) re-exports
the projection vault so the note's consequences are immediately visible in the
graph.

Notes may carry YAML frontmatter: `date:` becomes the decisions' valid_from
(recorded_at stays the ingest time — bi-temporal honesty: "what did you know,
and when"), and a `project:` key that names a DIFFERENT project makes the
watcher skip the note (a guard against notes dropped into the wrong inbox).
Files whose frontmatter says `generated-by: trace` are projections and are
never ingested — that is the loop-guard that keeps sources and projections
one-way.

Run:  python vault_watcher.py pearl-vista   (needs DASHSCOPE_API_KEY for capture)
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from typing import Optional

import yaml

from capture import capture_decision
from court import convene, render_verdict
from invalidate import check_invalidation, render_alert
from kb import KB_ROOT, export_vault
from store import Episode, add_decision, add_episode

POLL_SECONDS = 1.0

_FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a note into (frontmatter dict, body). Tolerant: no frontmatter, or
    unparseable frontmatter, yields ({}, whole text)."""
    m = _FM.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
        if not isinstance(fm, dict):
            fm = {}
    except yaml.YAMLError:
        fm = {}
    return fm, text[m.end():]


def ingest_note(conn, text: str, path: str = "", project: str = "",
                context: Optional[dict] = None, client=None, rules=None) -> Optional[dict]:
    """Ingest ONE note through the full pipeline. Returns a summary dict, or
    None when the note must not be ingested: a Trace projection (never ingest
    our own output), or a note whose frontmatter `project:` names a different
    project (wrong inbox). Dedupe is content-addressed: re-ingesting identical
    text is a no-op that returns the existing episode with no new decisions.
    `rules` is the project's rule-pack list (defaults to the SCDF pack)."""
    fm, body = parse_frontmatter(text)
    if str(fm.get("generated-by", "")).lower() == "trace":
        return None
    if project and fm.get("project") and str(fm["project"]) != project:
        return None

    episode = Episode(body=text, path=path, frontmatter=fm)
    before = conn.execute("SELECT COUNT(*) AS n FROM episodes").fetchone()["n"]
    episode = add_episode(conn, episode)
    after = conn.execute("SELECT COUNT(*) AS n FROM episodes").fetchone()["n"]
    if after == before:  # content already ingested (rename / re-save)
        return {"episode": episode.id, "duplicate": True,
                "captured": [], "alerts": [], "verdicts": []}

    # Bi-temporal honesty: the note's own date is when the decision became true
    # in the world (valid_from); ingestion time is when Trace learned it
    # (recorded_at, defaulted by the store).
    valid_from = str(fm["date"]) if fm.get("date") else None

    summary = {"episode": episode.id, "duplicate": False,
               "captured": [], "alerts": [], "verdicts": []}
    for c in capture_decision(body, source_episode=episode.id,
                              valid_from=valid_from, client=client):
        alerts = check_invalidation(conn, c, context=context, client=client, rules=rules)
        if alerts:
            c.decision.status = "proposed"
            add_decision(conn, c.decision)
            summary["alerts"].extend(render_alert(a) for a in alerts)
            # The evidence pass ran once, above — the court rules on THOSE
            # alerts (no second, possibly-disagreeing premise check).
            v = convene(conn, c, client=client, context=context, alerts=alerts)
            summary["verdicts"].append(render_verdict(v))
        else:
            add_decision(conn, c.decision)
        summary["captured"].append({"id": c.decision.id,
                                    "statement": c.decision.statement,
                                    "status": c.decision.status})
    return summary


def watch(project: str, conn=None, root: Optional[Path] = None, client=None,
          poll: float = POLL_SECONDS, max_polls: Optional[int] = None) -> None:
    """The polling loop. `max_polls` bounds the loop for tests; None = forever."""
    import os
    from scenarios import PROJECTS, build_store, project_rules
    if project not in PROJECTS:
        raise SystemExit(f"unknown project '{project}'; one of {list(PROJECTS)}")
    meta = PROJECTS[project]
    conn = conn or build_store(project)
    rules = project_rules(project)
    if client is None and os.getenv("DASHSCOPE_API_KEY"):
        # One shared client so capture AND the LLM premise half both run live.
        from capture import _client
        client = _client()
    root = Path(root) if root else KB_ROOT
    inbox = root / project / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    export_vault(conn, project, root, title=meta["title"])
    print(f"Trace vault watcher — {meta['title']}\n"
          f"  inbox:  {inbox}\n  vault:  {root / project}\n"
          f"  drop a markdown meeting note into the inbox…  (Ctrl+C to stop)")

    seen_mtimes: dict[Path, float] = {}
    polls = 0
    while max_polls is None or polls < max_polls:
        polls += 1
        for f in sorted(inbox.glob("*.md")):
            mtime = f.stat().st_mtime
            if seen_mtimes.get(f) == mtime:
                continue
            seen_mtimes[f] = mtime
            text = f.read_text(encoding="utf-8")
            out = ingest_note(conn, text, path=f"inbox/{f.name}", project=project,
                              context=meta.get("context"), client=client, rules=rules)
            if out is None or out["duplicate"]:
                continue
            print(f"\n⚡ ingested {f.name} as {out['episode']}")
            for c in out["captured"]:
                print(f"   captured {c['id']} [{c['status']}]  {c['statement'][:70]}")
            for a in out["alerts"]:
                print("\n" + a)
            for v in out["verdicts"]:
                print("\n" + v)
            export_vault(conn, project, root, title=meta["title"])
            print(f"\n   vault re-exported -> {root / project}")
        if max_polls is None or polls < max_polls:
            time.sleep(poll)


if __name__ == "__main__":
    watch(sys.argv[1] if len(sys.argv) > 1 else "tanglin-rise")
