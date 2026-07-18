"""The decision court — adversarial, reasoned invalidation (the innovation showpiece).

When a proposed decision trips the invalidation check, three Qwen roles deliberate:
  • Proposer — argues in favour of the change (cost / buildability)
  • Guardian — argues it breaks a prior decision's premise, citing the rule + decision
  • Judge    — decides the verdict and writes its rationale, as a defensible record

Verdicts are REAL state transitions, not just prose: REJECT marks the proposal
`rejected` on the record (never deleted); ALLOW adopts it as in force and, when
it displaces a conflicting prior decision, closes that decision as superseded.

Evidence comes in two strengths and the court treats them differently:
  • a rule-pack violation is deterministic law — the verdict is REJECT and the
    LLM writes the *reasoning* (reliable on camera, defensible for a QP);
  • an LLM premise-check alert is probabilistic evidence — here the Judge
    genuinely decides (ALLOW or REJECT, strict JSON), after hearing both sides.
Reuses check_invalidation (the evidence) + the Qwen stack.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from invalidate import check_invalidation
from store import (
    _append_audit, _now, add_decision, adopt_decision, get_decision,
    link_supersession, reject_decision,
)

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
    superseded: Optional[str] = None  # the id an ALLOW actually displaced (set only when linked)
    also: list = field(default_factory=list)  # the OTHER charges heard (multi-conflict proposals)


_PROPOSER = ("You are recording the contractor's position. In ONE sentence, restate the proposal's STATED "
             "COMMERCIAL RATIONALE (cost / buildability / 'or equivalent') as the contractor put it. You "
             "are reporting their commercial case, not evaluating fire safety or compliance. No caveats, "
             "no preamble.")
_GUARDIAN = ("You are the Guardian in an AEC design-decision review. In ONE sentence, argue that the "
             "proposed change breaks a prior decision's premise and is non-compliant — name the decision "
             "it breaks and cite the rule. No preamble.")
_JUDGE_RULE = ("You are the Judge, writing the record for a personally-liable Qualified Person. The cited "
               "rule is deterministic law, so the change is rejected; in ONE or TWO sentences, give the "
               "verdict rationale: why it is rejected, citing the clause and the decision it breaks. "
               "Write it as a defensible record. No preamble.")
_JUDGE_OPEN = ("You are the Judge in an AEC design-decision court, deciding for a personally-liable "
               "Qualified Person. No deterministic rule is violated — the evidence is that the proposal "
               "may falsify a stated premise of a prior decision. Weigh the Proposer's and Guardian's "
               "arguments and DECIDE. Reply with strict JSON, nothing else: "
               '{"verdict": "REJECT"|"ALLOW", "rationale": "<one or two sentences, citing the decision '
               'and premise, written as a defensible record>"}')


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


def _parse_judgment(text: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        out = json.loads(cleaned)
        return out if isinstance(out, dict) else {}
    except json.JSONDecodeError:
        return {}


def _persist(conn, captured, v: Verdict, created_at: Optional[str] = None) -> None:
    """Record the verdict on the trail — the court's 'defensible record' must
    itself be on the record, not just printed."""
    conn.execute(
        """INSERT INTO court_records
             (proposal_id, breaks_id, verdict, citation, for_argument,
              against_argument, rationale, created_at)
           VALUES (?,?,?,?,?,?,?,?)""",
        (captured.decision.id, v.breaks, v.verdict, v.citation,
         v.for_argument, v.against_argument, v.rationale, created_at or _now()),
    )
    _append_audit(conn, "verdict", captured.decision.id, {
        "verdict": v.verdict, "breaks": v.breaks, "citation": v.citation,
        "rationale": v.rationale,
    })
    conn.commit()


def get_court_records(conn) -> list[dict]:
    rows = conn.execute("SELECT * FROM court_records ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def _chain_tail(conn, decision_id: str):
    """Follow superseded_by links to the newest version of a decision."""
    d = get_decision(conn, decision_id)
    while d is not None and d.superseded_by:
        d = get_decision(conn, d.superseded_by)
    return d


def _apply(conn, captured, charges: list[Verdict], final: Optional[str] = None) -> None:
    """Make the verdict true on the record. Every charge's ruling is persisted
    FIRST — the audit chain must show the rulings before the state transition
    they authorize — then the proposal's single fate lands on its row: REJECT
    marks it rejected; ALLOW adopts it and supersedes EVERY in-force decision
    the charges displaced (each resolved to its chain tail, deduped)."""
    final = final or charges[0].verdict
    for v in charges:
        _persist(conn, captured, v)
    pid = captured.decision.id
    if final == "REJECT":
        reject_decision(conn, pid)
        return
    adopted = adopt_decision(conn, pid)
    linked: set[str] = set()
    for v in charges:
        if not v.breaks:
            continue
        # The charge's `breaks` may point mid-chain (a future-effective
        # supersession keeps an old version in force): link the chain tail,
        # and only claim a supersession that actually happened.
        target = _chain_tail(conn, v.breaks)
        if (target is not None and target.status == "valid"
                and target.id != adopted.id and target.id not in linked):
            link_supersession(conn, target.id, adopted.id)
            linked.add(target.id)
            v.superseded = target.id


def convene(conn, captured, client=None, model: str = MODEL, context: Optional[dict] = None,
            rules=None, alerts=None) -> Verdict:
    # The proposal under judgment must itself be on the record BEFORE the court
    # rules, so the verdict's proposal_id is real and the fate lands on that row.
    if captured.decision.id is None or get_decision(conn, captured.decision.id) is None:
        captured.decision.status = "proposed"
        add_decision(conn, captured.decision)

    # The evidence check needs the client BEFORE it runs: when the rule-pack is
    # silent, the LLM premise check IS the general half — without it, every
    # rule-silent premise break would sail through the court unexamined. Build
    # the default client only when a key exists, so offline stays offline.
    if client is None and os.getenv("DASHSCOPE_API_KEY"):
        client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)
    if alerts is None:  # a caller that already ran the check passes its alerts in
        alerts = check_invalidation(conn, captured, client=client, context=context, rules=rules)
    if not alerts:
        v = Verdict(False, "ALLOW", rationale="No prior premise is broken.")
        _apply(conn, captured, [v])
        return v

    # EVERY conflict is heard — a proposal that breaks several prior decisions'
    # premises gets one full deliberation (and one persisted court record) per
    # charge, not just the first.
    charges: list[Verdict] = []
    for alert in alerts:
        case = _case(captured, alert)
        proposer = _role(client, model, _PROPOSER, case)
        guardian = _role(client, model, _GUARDIAN, case)
        deliberation = f"{case}\n\nPROPOSER ARGUES: {proposer}\nGUARDIAN ARGUES: {guardian}"

        if alert.source == "rule":
            # Deterministic law: the rule-pack gates the verdict; the LLM writes the
            # defensible reasoning. This half can never mis-rule on camera.
            verdict, rationale = "REJECT", _role(client, model, _JUDGE_RULE, deliberation)
        else:
            # Probabilistic evidence: the Judge genuinely decides. An unparseable
            # ruling falls back to REJECT — with live evidence that a premise broke,
            # the conservative fate for a QP's record is to hold the proposal.
            ruling = _parse_judgment(_role(client, model, _JUDGE_OPEN, deliberation))
            verdict = ruling.get("verdict") if ruling.get("verdict") in ("REJECT", "ALLOW") else "REJECT"
            rationale = ruling.get("rationale") or guardian

        charges.append(Verdict(
            conflict=True, verdict=verdict,
            breaks=alert.breaks.id if alert.breaks else None,
            citation=alert.citation, for_argument=proposer,
            against_argument=guardian, rationale=rationale,
        ))

    # One proposal, one fate: ANY sustained charge rejects it; ALLOW requires
    # every charge to be ruled ALLOW. The returned verdict is the deciding
    # charge, carrying the other charges in `also`.
    primary = next((c for c in charges if c.verdict == "REJECT"), charges[0])
    primary.also = [c for c in charges if c is not primary]
    _apply(conn, captured, charges, final=primary.verdict)
    return primary


def render_verdict(v: Verdict) -> str:
    if not v.conflict:
        return f"COURT — ALLOW: {v.rationale}"
    lines = [f"DECISION COURT — VERDICT: {v.verdict}", "-" * 44,
             f"FOR  (Proposer): {v.for_argument}",
             f"AGAINST (Guardian): {v.against_argument}",
             f"JUDGE'S RATIONALE: {v.rationale}"]
    if v.superseded:  # only claim a supersession that was actually performed
        lines.append(f"SUPERSEDES: {v.superseded}  ·  {v.citation}")
    elif v.breaks:
        lines.append(f"BREAKS: {v.breaks}  ·  {v.citation}")
    for c in v.also:  # the other charges heard on the same proposal
        if c.superseded:
            lines.append(f"ALSO SUPERSEDES: {c.superseded}  ·  {c.citation}")
        elif c.breaks:
            lines.append(f"ALSO BREAKS: {c.breaks}  ·  {c.citation}")
    return "\n".join(lines)
