"""C1 — capture_decision: turn a meeting transcript into structured Decision records.

Uses Qwen function-calling (qwen-plus) to extract each firm design decision with
its rationale + assumptions (the "why" ordinary minutes drop). Returns Captured
= (Decision, attributes): the Decision goes to the store; `attributes` carries
machine-checkable facts (e.g. cladding combustibility) for the rule-pack, so the
spine schema stays untouched. See docs/02-architecture.md §4 Pipeline A.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

from dotenv import load_dotenv
from openai import OpenAI

from store import Decision

load_dotenv()

MODEL = "qwen-plus"
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

DISCIPLINES = [
    "architecture", "structural", "mep", "fire", "facade",
    "cost", "planning", "client",
]

RECORD_DECISION_TOOL = {
    "type": "function",
    "function": {
        "name": "record_decision",
        "description": "Record ONE firm design decision (or a firm proposal to change one) made in the meeting.",
        "parameters": {
            "type": "object",
            "properties": {
                "statement": {"type": "string", "description": "The decision in one sentence."},
                "discipline": {"type": "string", "enum": DISCIPLINES},
                "rationale": {"type": "string", "description": "WHY it was decided."},
                "assumptions": {
                    "type": "array", "items": {"type": "string"},
                    "description": "The premises the decision rests on.",
                },
                "author": {
                    "type": "array", "items": {"type": "string"},
                    "description": "Who made or owns the decision.",
                },
                "brief_ref": {"type": "string", "description": "Brief item / spec section affected, if stated."},
                "cladding_combustible": {
                    "type": ["boolean", "null"],
                    "description": (
                        "Only if this decision sets the external facade cladding: true if that "
                        "cladding is combustible (e.g. polyethylene / PE-core ACP), false if "
                        "non-combustible (e.g. A1 / mineral-core). Otherwise null."
                    ),
                },
                "inspection_competent_person": {
                    "type": ["boolean", "null"],
                    "description": (
                        "Only if this decision concerns the periodic facade inspection: false if "
                        "it skips or removes the appointed Competent Person (e.g. relies on "
                        "contractor drone footage alone), true if a Competent Person conducts "
                        "the inspection. Otherwise null."
                    ),
                },
                "inspection_within_cycle": {
                    "type": ["boolean", "null"],
                    "description": (
                        "Only if this decision schedules the periodic facade inspection: false if "
                        "it defers the inspection beyond the statutory 7-year cycle, true if it "
                        "stays within the cycle. Otherwise null."
                    ),
                },
            },
            "required": ["statement", "discipline", "rationale", "assumptions", "author"],
        },
    },
}

SYSTEM_PROMPT = """You are Trace, a design-decision memory agent for AEC (architecture / engineering / construction) projects.
Read the meeting transcript and identify each explicit design DECISION — a choice the team agreed, or a firm proposal to change a prior choice. For EACH decision, call record_decision once with the exact fields.
Capture the rationale (the WHY) and the assumptions the decision rests on. Record only firm decisions or firm proposals, not open discussion, questions, or asides. Do not invent decisions."""


@dataclass
class Captured:
    decision: Decision
    attributes: dict = field(default_factory=dict)


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)


def parse_tool_calls(tool_calls, *, source_episode="", recorded_at=None, valid_from=None) -> list[Captured]:
    """Deterministic mapping of record_decision tool-calls -> Captured. No network."""
    out: list[Captured] = []
    for tc in tool_calls or []:
        a = json.loads(tc.function.arguments)
        decision = Decision(
            statement=a["statement"],
            discipline=a.get("discipline", ""),
            rationale=a.get("rationale", ""),
            assumptions=a.get("assumptions", []),
            author=a.get("author", []),
            brief_ref=a.get("brief_ref", ""),
            source_episode=source_episode,
            recorded_at=recorded_at,
            valid_from=valid_from,
        )
        attributes = {}
        for key in ("cladding_combustible", "inspection_competent_person", "inspection_within_cycle"):
            if a.get(key) is not None:
                attributes[key] = a[key]
        out.append(Captured(decision, attributes))
    return out


def capture_decision(transcript, *, source_episode="", recorded_at=None, valid_from=None,
                     client=None, model=MODEL) -> list[Captured]:
    client = client or _client()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        tools=[RECORD_DECISION_TOOL],
        tool_choice="auto",
        temperature=0,
    )
    return parse_tool_calls(
        resp.choices[0].message.tool_calls,
        source_episode=source_episode, recorded_at=recorded_at, valid_from=valid_from,
    )
