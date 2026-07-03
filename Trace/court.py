"""The decision court — adversarial, reasoned invalidation (the innovation showpiece).

When a proposed decision trips the rule-pack, three Qwen roles deliberate:
  • Proposer — argues in favour of the change (cost / buildability)
  • Guardian — argues it breaks a prior decision's premise, citing the rule + decision
  • Judge    — writes the verdict rationale, as a defensible record

The rule-pack GATES the verdict (REJECT on a rule hit) so it's reliable on camera;
the LLM produces the *reasoning* — the trail a personally-liable QP stands behind.
Reuses check_invalidation (the deterministic evidence) + the Qwen stack.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from invalidate import check_invalidation
from store import _append_audit, _now

load_dotenv()

MODEL = "qwen-plus"
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"


@dataclass
class Verdict:
    conflict: bool
    verdict: str  # "REJECT" | "ALLOW"
    breaks: Optional[str] = None
    citation: str = ""
    for_argument: str = ""
    against_argument: str = ""
    rationale: str = ""


_PROPOSER = ("You are recording the contractor's position. In ONE sentence, restate the proposal's STATED "
             "COMMERCIAL RATIONALE (cost / buildability / 'or equivalent') as the contractor put it. You "
             "are reporting their commercial case, not evaluating fire safety or compliance. No caveats, "
             "no preamble.")
_GUARDIAN = ("You are the Guardian in an AEC design-decision review. In ONE sentence, argue that the "
             "proposed change breaks a prior decision's premise and is non-compliant — name the decision "
             "it breaks and cite the rule. No preamble.")
_JUDGE = ("You are the Judge, writing the record for a personally-liable Qualified Person. In ONE or TWO "
          "sentences, give the verdict rationale: why the change is rejected, citing the clause and the "
          "decision it breaks. Write it as a defensible record. No preamble.")


def _case(captured, alert) -> str:
    lines = [f"PROPOSED: {captured.decision.statement}"]
    if captured.decision.rationale:
        lines.append(f"STATED COMMERCIAL RATIONALE: {captured.decision.rationale}")
    if alert.breaks is not None:
        premise = alert.broken_premise or alert.breaks.rationale
        lines.append(f"BREAKS: {alert.breaks.id} — {alert.breaks.statement} (premise: {premise})")
    lines.append(f"RULE: {alert.rationale}  [{alert.citation}]")
    if alert.blast_radius:
        lines.append("CONSEQUENCE: " + ", ".join(alert.blast_radius))
    return "\n".join(lines)


def _role(client, model, system, case) -> str:
    resp = client.chat.completions.create(
        model=model, temperature=0,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": case}],
    )
    return resp.choices[0].message.content.strip()


def _persist(conn, captured, v: Verdict) -> None:
    """Record the verdict on the trail — the court's 'defensible record' must
    itself be on the record, not just printed."""
    conn.execute(
        """INSERT INTO court_records
             (proposal_id, breaks_id, verdict, citation, for_argument,
              against_argument, rationale, created_at)
           VALUES (?,?,?,?,?,?,?,?)""",
        (captured.decision.id, v.breaks, v.verdict, v.citation,
         v.for_argument, v.against_argument, v.rationale, _now()),
    )
    _append_audit(conn, "verdict", captured.decision.id, {
        "verdict": v.verdict, "breaks": v.breaks, "citation": v.citation,
        "rationale": v.rationale,
    })
    conn.commit()


def get_court_records(conn) -> list[dict]:
    rows = conn.execute("SELECT * FROM court_records ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def convene(conn, captured, client=None, model: str = MODEL) -> Verdict:
    alerts = check_invalidation(conn, captured)  # deterministic evidence
    if not alerts:
        v = Verdict(False, "ALLOW", rationale="No prior premise is broken.")
        _persist(conn, captured, v)
        return v
    alert = alerts[0]
    client = client or OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)
    case = _case(captured, alert)
    proposer = _role(client, model, _PROPOSER, case)
    guardian = _role(client, model, _GUARDIAN, case)
    rationale = _role(client, model, _JUDGE, f"{case}\n\nPROPOSER ARGUES: {proposer}\nGUARDIAN ARGUES: {guardian}")
    v = Verdict(
        conflict=True, verdict="REJECT",
        breaks=alert.breaks.id if alert.breaks else None,
        citation=alert.citation, for_argument=proposer,
        against_argument=guardian, rationale=rationale,
    )
    _persist(conn, captured, v)
    return v


def render_verdict(v: Verdict) -> str:
    if not v.conflict:
        return f"COURT — ALLOW: {v.rationale}"
    lines = [f"DECISION COURT — VERDICT: {v.verdict}", "-" * 44,
             f"FOR  (Proposer): {v.for_argument}",
             f"AGAINST (Guardian): {v.against_argument}",
             f"JUDGE'S RATIONALE: {v.rationale}"]
    if v.breaks:
        lines.append(f"BREAKS: {v.breaks}  ·  {v.citation}")
    return "\n".join(lines)
