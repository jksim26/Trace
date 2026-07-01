"""C5 — expose Trace's core functions as Qwen-Agent tools (the MCP / custom-skills
judging hook). Registers capture_decision, check_invalidation, recall_decisions,
and supersede_decision as @register_tool classes over a shared in-memory store,
so a Qwen-Agent Assistant can call them as tools. See docs/02 §5.
"""
from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from qwen_agent.tools.base import BaseTool, register_tool

from capture import Captured, capture_decision as _capture
from invalidate import check_invalidation as _check, render_alert
from recall import recall_decisions as _recall
from store import (
    Decision, add_decision, connect, get_history, init_db,
    supersede_decision as _supersede,
)

load_dotenv()

BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
_conn = None


def _get_conn():
    global _conn
    if _conn is None:
        _conn = connect(":memory:")
        init_db(_conn)
    return _conn


def reset_store():
    """Drop the shared store (fresh :memory: db) — used by tests and demo runs."""
    global _conn
    _conn = None


def _args(params):
    return json.loads(params) if isinstance(params, str) else params


@register_tool("capture_decision")
class CaptureDecision(BaseTool):
    description = "Extract and store the design decision(s) in a meeting transcript, with rationale and assumptions."
    parameters = [
        {"name": "transcript", "type": "string", "description": "The meeting transcript text.", "required": True},
    ]

    def call(self, params, **kwargs) -> str:
        conn = _get_conn()
        captured = []
        for c in _capture(_args(params)["transcript"]):
            d = add_decision(conn, c.decision)
            captured.append({"id": d.id, "statement": d.statement, "attributes": c.attributes})
        return json.dumps({"captured": captured})


@register_tool("check_invalidation")
class CheckInvalidation(BaseTool):
    description = ("Check whether a proposed facade-cladding decision breaks a live premise "
                  "(e.g. non-combustible required over 15 m). Returns any invalidation alert.")
    parameters = [
        {"name": "statement", "type": "string", "description": "The proposed decision.", "required": True},
        {"name": "cladding_combustible", "type": "boolean",
         "description": "True if the proposed cladding is combustible (e.g. polyethylene / PE-core ACP).",
         "required": True},
    ]

    def call(self, params, **kwargs) -> str:
        a = _args(params)
        cap = Captured(
            Decision(statement=a["statement"], discipline="facade"),
            {"cladding_combustible": a["cladding_combustible"]},
        )
        alerts = _check(_get_conn(), cap)
        return json.dumps({"conflict": bool(alerts), "alerts": [render_alert(x) for x in alerts]})


@register_tool("recall_decisions")
class RecallDecisions(BaseTool):
    description = "Answer a question from currently-valid design decisions within a token budget; abstain if nothing is on record."
    parameters = [
        {"name": "question", "type": "string", "description": "The question to answer.", "required": True},
    ]

    def call(self, params, **kwargs) -> str:
        r = _recall(_get_conn(), _args(params)["question"])
        return json.dumps({"answer": r.answer, "cited": r.cited, "tokens_used": r.used, "abstained": r.abstained})


@register_tool("supersede_decision")
class SupersedeDecision(BaseTool):
    description = "Supersede an existing decision with a new one, preserving the old (never deleted) via a superseded_by link."
    parameters = [
        {"name": "old_id", "type": "string", "description": "The decision id to supersede, e.g. D-001.", "required": True},
        {"name": "new_statement", "type": "string", "description": "The replacement decision.", "required": True},
    ]

    def call(self, params, **kwargs) -> str:
        a = _args(params)
        new = _supersede(_get_conn(), a["old_id"], Decision(statement=a["new_statement"], discipline="facade"))
        chain = get_history(_get_conn(), a["old_id"])
        return json.dumps({"new_id": new.id, "chain": [{"id": d.id, "status": d.status} for d in chain]})


def build_agent():
    from qwen_agent.agents import Assistant
    return Assistant(
        llm={"model": "qwen-plus", "model_server": BASE_URL, "api_key": os.getenv("DASHSCOPE_API_KEY")},
        function_list=["capture_decision", "check_invalidation", "recall_decisions", "supersede_decision"],
        system_message=(
            "You are Trace, a design-decision memory agent for AEC projects. Use the tools: capture "
            "decisions from transcripts, check a proposed cladding change for invalidation (PE-core ACP "
            "is combustible), and recall decisions. Always call the appropriate tool."
        ),
    )


if __name__ == "__main__":
    from pathlib import Path
    reset_store()
    t1 = (Path(__file__).resolve().parent.parent / "demo/transcripts/01-concept-design-2026-01-14.md").read_text(encoding="utf-8")
    agent = build_agent()
    msgs = [{"role": "user", "content":
             f"Here is a concept-design meeting transcript. Capture the decision(s):\n\n{t1}\n\n"
             "Then check whether a value-engineering proposal to switch the facade to polyethylene-core ACP "
             "would break any prior decision."}]
    final = []
    for rsp in agent.run(messages=msgs):
        final = rsp  # each yield is the full, growing message list
    called = [m["function_call"]["name"] for m in final if m.get("function_call")]
    print("TOOLS CALLED BY THE AGENT:", called)
    print("FINAL:", final[-1].get("content", "")[:400])
