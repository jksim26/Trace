"""The ambient trigger — ONE brain for BOTH worlds.

match_title() maps a window/document title to a project context. It is called
by BOTH trigger paths, so the browser workspace demo and the real Windows
watcher are provably the same logic:

  • watcher.py (Windows)  — real foreground window titles ("...pdf - Adobe
    Acrobat", "... - Autodesk Revit") polled from the OS
  • bubble.py /nudge      — document-open events from the simulated workspace
    page (the drawings are demo files; Trace's reaction is live)

Rules live in watch_rules.yaml — an ALLOWLIST: anything that matches no rule
is ignored and never leaves the machine. Deterministic by design: "this title
is the Level 1 fire plan" is a fact, not a judgment.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

_RULES_PATH = Path(__file__).with_name("watch_rules.yaml")


@dataclass
class Match:
    project: str
    context: str
    keywords: str


def load_watch_rules(path=None) -> list[dict]:
    p = Path(path) if path else _RULES_PATH
    return yaml.safe_load(p.read_text(encoding="utf-8")) or []


def match_title(title: str, rules: Optional[list] = None) -> Optional[Match]:
    """First matching allowlist rule wins; no rule -> None (ignored)."""
    if not title:
        return None
    rules = rules if rules is not None else load_watch_rules()
    for r in rules:
        if re.search(r["pattern"], title, re.IGNORECASE):
            return Match(r["project"], r["context"], r.get("keywords", ""))
    return None
