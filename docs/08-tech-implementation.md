# 07 · Technology Implementation Guide — TRACE

*What technologies are needed to build each part of TRACE, with multiple implementation options per module.*
*Written for a 2–3 person team new to AI development. Difficulty ratings and time estimates are calibrated for this team profile.*
*Confidence tags: `[verified]` · `[web search]` · `[inference]`*

---

## How to Read This Document

Each section covers **one functional module** of TRACE. For every module, you will find:

- **What it needs to do** — the job this module performs
- **Option A · Recommended** — the fastest, safest path for a hackathon
- **Option B · Alternative** — a different approach with different trade-offs
- **Option C · Stretch / Production** — what this would look like if you had more time or were building for real
- **Difficulty rating** — ★☆☆☆☆ (beginner) to ★★★★★ (expert)
- **Time estimate** — for a 2–3 person team, AI-newcomer profile, working ~8–10 hours/day

### Difficulty Scale
| Rating | Meaning |
|---|---|
| ★☆☆☆☆ | Copy-paste and configure; no coding knowledge needed |
| ★★☆☆☆ | Simple Python scripting; a few hours of learning |
| ★★★☆☆ | Moderate coding; requires debugging and reading docs |
| ★★★★☆ | Complex integration; significant debugging expected |
| ★★★★★ | Expert-level; not recommended for hackathon timeline |

### Team Assumption
All estimates assume **2–3 people**, splitting work in parallel where possible, working ~8–10 hours/day. Where a task is labelled `[parallel]`, two people can work on it simultaneously to cut clock time.

---

## Module 0 · Project Scaffolding & Environment Setup

**What it needs to do:** Create the repo, install dependencies, connect to Qwen Cloud, verify the API works, set up the project folder structure.

### Option A · Recommended — Python + pip + `.env` file ★★☆☆☆
**Tools:** Python 3.11+, `pip`, `python-dotenv`, `openai` SDK (reused for Qwen's OpenAI-compatible endpoint)

```
trace/
├── main.py                  # CLI entry point
├── .env                     # DASHSCOPE_API_KEY=...  (never commit this)
├── requirements.txt
├── trace/
│   ├── schema.py            # Decision dataclass
│   ├── store.py             # SQLite read/write
│   ├── capture.py           # capture_decision tool
│   ├── invalidate.py        # check_invalidation tool
│   ├── recall.py            # recall_decisions tool
│   └── rules/
│       └── fire.yaml        # AEC rule-pack
├── transcripts/             # Maple Wharf .txt files
└── README.md
```

Install in one command:
```bash
pip install openai python-dotenv pyyaml sqlite-vec rich
```

**Time estimate:** 2–3 hours (one person sets up while another writes the schema)
**Risk:** Low. This is standard Python project setup.

### Option B · Alternative — Poetry for dependency management ★★☆☆☆
Same as Option A but uses `poetry` instead of `pip`. Cleaner dependency locking, better for teams. Slightly longer setup (~1 extra hour to learn Poetry if unfamiliar).

**Time estimate:** 3–4 hours
**Recommended only if:** you already use Poetry; otherwise stick with pip.

### Option C · Stretch — Docker container ★★★☆☆
Wrap everything in a Docker container so judges can run it with one command (`docker run trace`). Impressive for the submission, but only worth doing after the core demo works.

**Time estimate:** 4–6 hours (after the app is working)

---

## Module 1 · Decision Storage — The Memory Spine

**What it needs to do:** Store every Decision record (statement, rationale, assumptions, author, timestamps, status). Never delete — only mark as superseded. Support querying by `valid_to IS NULL` (currently active) and full history retrieval for the audit trail.

### Option A · Recommended — SQLite + Python `sqlite3` ★★☆☆☆

SQLite is a file-based database. Think of it as a very structured spreadsheet that lives in a single file (`trace.db`) and can be queried with standard SQL. No server, no installation beyond Python's built-in library.

**Why this wins for the hackathon:**
- Zero setup — Python includes `sqlite3` in its standard library
- Easy to open and inspect visually with [DB Browser for SQLite](https://sqlitebrowser.org/) (free GUI tool)
- Trivially included in an open-source repo — judges can run it on their laptop
- Fast enough for one project's decisions (likely < 500 rows)

```sql
-- Core table (simplified)
CREATE TABLE decisions (
    id            TEXT PRIMARY KEY,       -- "D-047"
    statement     TEXT NOT NULL,
    rationale     TEXT,
    assumptions   TEXT,                   -- JSON array stored as text
    author        TEXT,
    discipline    TEXT,
    riba_stage    INTEGER,
    importance    INTEGER DEFAULT 3,
    valid_from    TEXT NOT NULL,          -- ISO 8601 datetime
    valid_to      TEXT,                   -- NULL = currently active
    recorded_at   TEXT NOT NULL,
    superseded_at TEXT,
    superseded_by TEXT,                   -- FK to another decision id
    status        TEXT DEFAULT 'valid',   -- 'valid' | 'superseded' | 'proposed'
    source_episode TEXT
);
```

**The golden rule: never DELETE.** To retire a decision:
```python
# WRONG — destroys the audit trail
cursor.execute("DELETE FROM decisions WHERE id = ?", (old_id,))

# RIGHT — the golden-thread-compliant way
cursor.execute("""
    UPDATE decisions
    SET valid_to = ?, superseded_at = ?, superseded_by = ?, status = 'superseded'
    WHERE id = ?
""", (new_decision_valid_from, now(), new_id, old_id))
```

**Time estimate:** 4–6 hours (schema design + write/read helpers + tests)
**Difficulty:** ★★☆☆☆

### Option B · Alternative — TinyDB (pure Python, no SQL) ★★☆☆☆

TinyDB stores records as a JSON file. No SQL syntax needed — you query with Python dictionaries. Much simpler to write initially, but harder to query efficiently as the record count grows.

```python
from tinydb import TinyDB, Query
db = TinyDB('trace.db.json')
Decision = Query()
active = db.search(Decision.valid_to == None)
```

**Trade-off:** Easier to start, harder to scale. Joins and complex queries become awkward. BFS traversal for blast radius (Module 5) is clunkier.
**Recommended if:** SQL feels intimidating and the team prioritises speed over query power.

**Time estimate:** 2–4 hours
**Difficulty:** ★★☆☆☆

### Option C · Stretch / Production — Neo4j graph database ★★★★☆

Neo4j is a true graph database where nodes (Decisions) and edges (ASSUMES, DEPENDS_ON, SUPERSEDED_BY) are first-class citizens. Querying "what does D-047 depend on?" becomes a single Cypher query instead of manual BFS code.

```cypher
MATCH (d:Decision {id: 'D-047'})-[:DEPENDS_ON*]->(downstream)
WHERE downstream.valid_to IS NULL
RETURN downstream
```

**Why not for the hackathon:** Requires running a Neo4j server (Docker or cloud), adds significant setup time, and the query advantages only matter when you have hundreds of decisions with complex dependency chains. Cite it as the production path in your deck — but build on SQLite.

**Time estimate:** 2–3 days (including learning Cypher)
**Difficulty:** ★★★★☆

---

## Module 2 · Decision Extraction — Turning Transcripts into Records

**What it needs to do:** Take raw meeting transcript text as input, and output one or more structured Decision records — correctly identifying the statement, rationale, assumptions, author, and discipline. This is the `capture_decision` tool.

### Option A · Recommended — Qwen function-calling with a strict JSON schema ★★★☆☆

Feed the transcript to `qwen3.7-max` (or `qwen-plus` for cost saving) with a **system prompt** that explains what a Decision is, and a **function/tool definition** that forces the model to output a structured JSON object matching the Decision schema.

Function-calling is like telling the model: "Don't just answer in prose — fill in this specific form." The model returns a machine-readable JSON object, not free text.

```python
EXTRACT_TOOL = {
    "type": "function",
    "function": {
        "name": "capture_decision",
        "description": "Extract a design decision from AEC meeting transcript text",
        "parameters": {
            "type": "object",
            "properties": {
                "statement":   {"type": "string", "description": "The decision made, in one sentence"},
                "rationale":   {"type": "string", "description": "Why this decision was made"},
                "assumptions": {"type": "array",  "items": {"type": "string"},
                                "description": "What must remain true for this decision to hold"},
                "author":      {"type": "string", "description": "Name and role of decision-maker"},
                "discipline":  {"type": "string", "enum": ["architecture","structural","mep",
                                                            "fire","facade","cost","planning","client"]},
                "riba_stage":  {"type": "integer", "description": "RIBA stage 0–7"}
            },
            "required": ["statement", "rationale", "assumptions", "author", "discipline"]
        }
    }
}
```

**System prompt approach:**
```python
SYSTEM_PROMPT = """
You are TRACE, a design-decision memory agent for AEC projects.
When given a meeting transcript chunk, identify all design decisions made.
For each decision, call capture_decision() with the exact fields requested.
A 'decision' is a choice that: (a) was explicitly agreed by the team,
(b) has a reason (rationale), and (c) rests on at least one assumption
that could later be violated.
Do not capture tentative suggestions or open questions as decisions.
"""
```

**Time estimate:** 6–10 hours (writing + testing on the Maple Wharf transcripts until extraction quality is good)
**Difficulty:** ★★★☆☆
**Main challenge:** Getting the prompt right so the model extracts cleanly and doesn't miss decisions or hallucinate extras. Budget 3–4 iterations.

### Option B · Alternative — Two-step extraction (simpler prompt, then parse) ★★☆☆☆

Step 1: Ask the model to list decisions in plain prose.
Step 2: Ask it to re-format each one as JSON.

This is less elegant but often easier to debug when the single-step approach produces messy output.

```python
# Step 1
prose = ask_llm("List every design decision made in this transcript. "
                "For each, give: what was decided, why, and by whom.")

# Step 2
structured = ask_llm(f"Convert each item below into JSON with fields: "
                     f"statement, rationale, assumptions, author, discipline.\n\n{prose}")
```

**Trade-off:** Two API calls instead of one (doubles cost for this step). Easier to debug.
**Time estimate:** 4–6 hours
**Difficulty:** ★★☆☆☆

### Option C · Stretch — Fine-tuned extraction model ★★★★★

Fine-tune a smaller Qwen model specifically on AEC decision extraction, using a hand-labelled dataset of transcripts. Massively better accuracy, much lower inference cost.

**Why not for the hackathon:** Requires labelled training data (which you don't have), fine-tuning infrastructure, and weeks of iteration. Post-hackathon opportunity only.

**Time estimate:** 2–4 weeks minimum
**Difficulty:** ★★★★★

---

## Module 3 · Vector Embeddings & Similarity Search

**What it needs to do:** Convert every stored decision (statement + rationale) into a numerical vector (embedding), store those vectors, and efficiently find which existing decisions are semantically similar to a new one — so the contradiction check knows *which* prior decisions to compare against.

Think of embeddings like GPS coordinates for meaning. Two decisions about the same facade material will have coordinates close together, even if they use different words.

### Option A · Recommended — Qwen `text-embedding-v4` + `sqlite-vec` ★★★☆☆

Use Qwen's hosted embedding model (no extra infrastructure) and store vectors in SQLite using the `sqlite-vec` extension (a plugin that adds vector search to SQLite).

```python
from openai import OpenAI
import sqlite_vec

# Embed a decision
client = OpenAI(api_key=..., base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

def embed(text: str) -> list[float]:
    resp = client.embeddings.create(
        model="text-embedding-v4",
        input=text,
        dimensions=1024,          # cost/quality sweet spot
        extra_body={"text_type": "document"}   # "query" for search queries
    )
    return resp.data[0].embedding

# Store in SQLite (sqlite-vec handles the index)
# Retrieve top-5 most similar to a new decision
```

**Why sqlite-vec:** Keeps everything in one SQLite file. No separate vector database to run. Fast enough for < 1,000 decisions.

**Time estimate:** 4–6 hours (including learning sqlite-vec)
**Difficulty:** ★★★☆☆

### Option B · Alternative — ChromaDB (dedicated vector store) ★★★☆☆

ChromaDB is a lightweight vector database that runs in-process (no server needed). More feature-rich than sqlite-vec but adds a dependency.

```python
import chromadb
client = chromadb.Client()
collection = client.create_collection("decisions")

# Add a decision embedding
collection.add(
    documents=["Facade = terracotta rainscreen on A2 mineral wool"],
    embeddings=[embed("Facade = terracotta rainscreen...")],
    ids=["D-047"]
)

# Search for similar decisions
results = collection.query(query_embeddings=[embed(new_decision)], n_results=5)
```

**Trade-off:** Slightly easier API than sqlite-vec, but now you have two databases (SQLite for decisions, Chroma for vectors). Synchronisation between them requires care.

**Time estimate:** 4–6 hours
**Difficulty:** ★★★☆☆

### Option C · Stretch / Production — Alibaba DashVector ★★★★☆

Alibaba's managed vector database service, designed to pair with DashScope/Qwen. Scales to millions of vectors, production-grade. Cited in the architecture docs as the production path alongside Neo4j.

**Why not for the hackathon:** Requires provisioning a cloud service, adds latency, and is overkill for a demo with < 500 decisions. Use DashVector in your deck's "production architecture" slide.

**Time estimate:** 1–2 days (provisioning + integration)
**Difficulty:** ★★★★☆

---

## Module 4 · The Contradiction / Invalidation Engine

**What it needs to do:** When a new decision arrives, determine whether it breaks the assumptions of any existing valid decision, and if so, fire an alert. This is the heart of TRACE — the `check_invalidation` tool. It has two parts working together: a deterministic rule-pack and an LLM premise checker.

### Option A · Recommended — YAML rule-pack + LLM premise check ★★★☆☆

**Part 1 — The rule-pack (deterministic, never misfires):**

A small YAML file encoding hard AEC constraints. When a new decision triggers a rule, the alert fires with certainty — no LLM involved.

```yaml
# rules/fire.yaml
- id: ADB-B4-noncombustible
  trigger_keywords: ["ACM", "aluminium composite", "combustible", "cladding"]
  applies_if: building_is_HRB  # height > 18m flag set at project creation
  constraint: "cladding must be rated A1 or A2-s1,d0"
  violated_by: ["ACM", "timber rainscreen", "GRP", "HPL"]
  prior_decision_field: "assumptions"
  alert_message: "NEW DECISION violates Approved Document B (B4): combustible cladding prohibited on HRBs (>18m). Prior decision D-{id} assumed non-combustible cladding."
  blast_radius:
    - "Structural: recalculate support brackets for new material dead load"
    - "Fire: cavity barriers and fire-stopping require re-specification"
    - "Energy: Part L U-value calculation must be re-run"
    - "Regulatory: Gateway 2 pre-construction submission must be updated"
```

```python
import yaml

def rule_pack_check(new_decision: dict, existing_decisions: list[dict]) -> list[dict]:
    """Returns list of conflicts found by the rule-pack."""
    rules = yaml.safe_load(open("rules/fire.yaml"))
    conflicts = []
    for rule in rules:
        # Check if new decision triggers this rule
        text = (new_decision["statement"] + " " + new_decision["rationale"]).lower()
        if any(kw.lower() in text for kw in rule["trigger_keywords"]):
            # Find prior decisions whose assumptions this violates
            for prior in existing_decisions:
                if prior["status"] == "valid" and rule["id"] in str(prior.get("assumptions", "")):
                    conflicts.append({"rule": rule, "prior": prior})
    return conflicts
```

**Part 2 — LLM premise check (catches what rules miss):**

For everything the rule-pack doesn't cover, ask `qwen3.7-max` to reason about whether the new decision breaks any assumption of the top-5 semantically similar prior decisions.

```python
PREMISE_CHECK_PROMPT = """
You are checking whether a NEW DESIGN DECISION invalidates any PRIOR DECISION.

NEW DECISION:
Statement: {new_statement}
Rationale: {new_rationale}

PRIOR DECISION (ID: {prior_id}):
Statement: {prior_statement}
Assumptions it rests on: {prior_assumptions}

Does the NEW DECISION directly violate or falsify any assumption the PRIOR DECISION relies on?
Answer JSON only: {{"conflict": true/false, "reason": "..."}}
"""
```

**Alert output format (what judges see on screen):**
```
⚠️  TRACE INVALIDATION ALERT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEW:   "Facade changed to ACM aluminium composite cladding" (D-089)
       Proposed by: J. Park (contractor value engineer), 2026-03-15

BREAKS: Decision D-047 — "Facade = terracotta on A2-s1,d0 mineral wool"
        Made by: R. Wells (arch) + P. Desai (fire), 2026-01-14
        Rationale: "HRB >18m; combustible cladding illegal per Approved Doc B"
        Violated assumption: "combustible cladding prohibited over 18m"

BLAST RADIUS:
  • Structural: support brackets must be recalculated for ACM dead load
  • Fire: cavity barriers and fire-stopping require re-specification
  • Energy: Part L U-value model must be re-run
  • Regulatory: Gateway 2 submission must be updated before construction

ACTION REQUIRED: Supersede D-047 and confirm Gateway 2 re-submission? [Y/N]
```

**Time estimate:**
- Rule-pack (YAML + checker function): 4–6 hours `[parallel]`
- LLM premise check (prompt + integration): 6–8 hours `[parallel]`
- Integration + testing on Maple Wharf storyline: 4–6 hours
- **Total: ~1.5–2 days (with parallel work)**

**Difficulty:** ★★★☆☆

### Option B · Alternative — Pure LLM detection (no rule-pack) ★★★☆☆

Skip the YAML rule-pack entirely. Feed all top-k similar prior decisions to the LLM and ask it to identify any conflicts.

**Advantage:** Less up-front engineering. Generalises to any domain.
**Risk:** LLM responses are probabilistic — the demo alert may fire inconsistently or produce verbose, hard-to-parse output. **Not recommended for the live demo recording.**

**Mitigation if you go this route:** Use the LLM in a chain-of-thought mode, then extract the final `conflict: true/false` with a second structured call.

**Time estimate:** 4–8 hours
**Difficulty:** ★★★☆☆

### Option C · Stretch — Automated dependency graph inference ★★★★☆

Instead of manually writing `DEPENDS_ON` edges or relying solely on keyword matching, train or prompt a model to infer which prior decisions a new decision depends on, and automatically populate the blast-radius graph.

**Why not for the hackathon:** The blast-radius edges in the demo are best hard-coded for the storyline (they will always be correct and film well). Automatic inference adds complexity and potential inaccuracy.

**Time estimate:** 3–5 days
**Difficulty:** ★★★★☆

---

## Module 5 · Recall Pipeline — Answering Questions Within a Token Budget

**What it needs to do:** Given a question ("Why did we choose terracotta, and can we still change it?"), retrieve the most relevant, currently-valid decisions, rank them, and pack only what fits a token budget — then answer. Show a visible context-budget meter. This is the `recall_decisions` tool.

### Option A · Recommended — Hybrid retrieval + composite scoring + greedy packing ★★★☆☆

Three steps in sequence:

**Step 1: Hybrid retrieval** (dense vector search + BM25 keyword search)
```python
def hybrid_retrieve(query: str, top_k: int = 20) -> list[dict]:
    # Dense: cosine similarity using embeddings
    query_vec = embed(query, text_type="query")
    dense_results = vector_search(query_vec, top_k=top_k)

    # Sparse: BM25 keyword matching using `rank_bm25` library
    from rank_bm25 import BM25Okapi
    corpus = [d["statement"] + " " + d["rationale"] for d in all_active_decisions()]
    bm25 = BM25Okapi([doc.split() for doc in corpus])
    sparse_scores = bm25.get_scores(query.split())

    # Merge: simple reciprocal rank fusion
    return merge_and_deduplicate(dense_results, sparse_scores)
```

**Step 2: Rerank with Qwen**
```python
# Send top-20 to qwen3-rerank, get back top-5 in relevance order
reranked = rerank_with_qwen(query, candidates[:20])
```

**Step 3: Composite re-score and greedy budget packing**
```python
import math, datetime

def composite_score(decision: dict, query_relevance: float) -> float:
    # Relevance: from reranker (0–1)
    relevance = query_relevance

    # Recency: exponential decay from valid_from date
    days_old = (datetime.now() - parse_date(decision["valid_from"])).days
    recency = math.exp(-0.01 * days_old)  # half-life ~70 days

    # Importance: deterministic 1–5 by decision type (set at capture time)
    importance = decision["importance"] / 5.0

    return (0.5 * relevance) + (0.3 * recency) + (0.2 * importance)

TOKEN_BUDGET = 4000  # tokens reserved for context

def retrieve_to_budget(ranked: list[dict]) -> list[dict]:
    packed, used = [], 0
    for d in ranked:
        tokens = estimate_tokens(d)  # rough: len(text) // 4
        if used + tokens > TOKEN_BUDGET:
            break
        packed.append(d)
        used += tokens
    return packed, used  # used drives the context-budget meter
```

**The context-budget meter (visible on screen during demo):**
```python
from rich.progress import Progress

def show_budget_meter(used: int, total: int = TOKEN_BUDGET):
    pct = used / total
    bar = "█" * int(pct * 30) + "░" * (30 - int(pct * 30))
    print(f"Context budget: [{bar}] {used}/{total} tokens ({pct*100:.0f}%)")
```

**Abstention (honest "no record" response):**
```python
if not packed:
    print("TRACE: No decision on record for this query. "
          "Either it was never decided, or it predates this project's memory.")
```

**Time estimate:** 8–12 hours (hybrid retrieval + rerank integration + budget meter + abstention)
**Difficulty:** ★★★☆☆

### Option B · Alternative — Simple vector-only retrieval ★★☆☆☆

Skip BM25 and reranking. Just use cosine similarity from the vector index, take top-5, and pack them.

**Trade-off:** Faster to build (2–4 hours), but retrieval quality is lower. May miss decisions that use different vocabulary for the same concept (BM25 catches exact keyword matches that dense search misses).

**Recommended if:** time is running out and you need to get Module 5 working quickly. Upgrade to hybrid later.

**Time estimate:** 2–4 hours
**Difficulty:** ★★☆☆☆

### Option C · Stretch — LongMemEval-style evaluation harness ★★★★☆

Build an automated test harness that scores TRACE's recall quality on a set of gold-standard question-answer pairs from the Maple Wharf transcripts. Measures: knowledge-update accuracy, temporal reasoning, abstention rate.

**Why not for the hackathon core:** The demo is manually verified against a controlled storyline — a formal eval harness is impressive but not required to win. Park this as a post-hackathon credibility builder.

**Time estimate:** 1–2 days
**Difficulty:** ★★★★☆

---

## Module 6 · Audit Trail & History View

**What it needs to do:** Show that superseded decisions are preserved with a full chain (Decision D-047 → superseded by D-089 → etc.), not deleted. This is the `audit trail` view and directly satisfies the golden-thread immutability requirement.

### Option A · Recommended — SQLite BFS traversal + `rich` table display ★★☆☆☆

Walk the `superseded_by` chain with a simple recursive query and display it as a formatted table in the terminal.

```python
def get_history_chain(decision_id: str) -> list[dict]:
    """Walk the superseded_by chain from root to latest."""
    chain = []
    current = get_decision(decision_id)
    while current:
        chain.append(current)
        current = get_decision(current.get("superseded_by"))
    return chain

def display_audit_trail(chain: list[dict]):
    from rich.table import Table
    from rich.console import Console
    console = Console()
    table = Table(title=f"Audit Trail — Decision {chain[0]['id']}")
    table.add_column("ID"); table.add_column("Status"); table.add_column("Valid From")
    table.add_column("Valid To"); table.add_column("Statement")
    for d in chain:
        status_colour = "green" if d["status"] == "valid" else "red"
        table.add_row(d["id"], f"[{status_colour}]{d['status']}[/]",
                      d["valid_from"], d["valid_to"] or "—", d["statement"][:60])
    console.print(table)
```

**Output on screen:**
```
Audit Trail — Decision D-047
┌───────┬────────────┬──────────────────────┬──────────────────────┬───────────────────────────┐
│ ID    │ Status     │ Valid From           │ Valid To             │ Statement                 │
├───────┼────────────┼──────────────────────┼──────────────────────┼───────────────────────────┤
│ D-047 │ superseded │ 2026-01-14 11:42Z    │ 2026-03-15 09:10Z   │ Facade = terracotta on... │
│ D-089 │ valid      │ 2026-03-15 09:10Z    │ —                   │ Facade changed to ACM...  │
└───────┴────────────┴──────────────────────┴──────────────────────┴───────────────────────────┘
```

**Time estimate:** 3–5 hours
**Difficulty:** ★★☆☆☆

### Option B · Alternative — Web-based audit view (Flask/FastAPI) ★★★☆☆

Serve a simple HTML page that renders the decision history as a visual timeline or table. More photogenic for the demo video than a terminal table.

```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/audit/<decision_id>")
def audit(decision_id):
    chain = get_history_chain(decision_id)
    return render_template("audit.html", chain=chain)
```

**Trade-off:** ~4–8 additional hours to build the web server and HTML template. Worth it if you want the demo to look polished for the video. Do this *after* the CLI version works.

**Time estimate:** 6–10 hours (including CLI version as base)
**Difficulty:** ★★★☆☆

### Option C · Stretch — Interactive graph visualisation ★★★★☆

Use `networkx` + `pyvis` (Python) or a JavaScript library (D3.js, Cytoscape.js) to render the decision dependency graph as an interactive node-link diagram. Clicking a node shows its audit trail; red nodes = superseded; green = active.

**Time estimate:** 1–2 days
**Difficulty:** ★★★★☆

---

## Module 7 · Qwen-Agent MCP Tool Wrapping

**What it needs to do:** Expose TRACE's four core functions as callable tools within the Qwen-Agent framework, so the agent visibly calls them as tools during the demo. This directly banks the "custom skills / MCP integrations" judging criterion (worth up to 30% of the score).

### Option A · Recommended — Qwen-Agent `@register_tool` decorator ★★★☆☆

Qwen-Agent allows you to define custom tools using a simple decorator. The agent framework then handles tool-calling, JSON parsing, and orchestration automatically.

```bash
pip install "qwen-agent[mcp]"
```

```python
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool("capture_decision")
class CaptureDecisionTool(BaseTool):
    description = "Extract and store a design decision from AEC meeting transcript text"
    parameters = [{
        "name": "transcript_chunk",
        "type": "string",
        "description": "Raw text from a meeting transcript",
        "required": True
    }]

    def call(self, params: dict, **kwargs) -> str:
        transcript = params["transcript_chunk"]
        decision = extract_decision_via_llm(transcript)   # Module 2
        store_decision(decision)                           # Module 1
        conflict = check_invalidation(decision)            # Module 4
        if conflict:
            return f"⚠️ CONFLICT DETECTED: {conflict['alert_message']}"
        return f"✅ Decision captured: {decision['id']} — {decision['statement']}"


@register_tool("recall_decisions")
class RecallDecisionsTool(BaseTool):
    description = "Retrieve currently-valid design decisions relevant to a query, within a token budget"
    parameters = [{
        "name": "query",
        "type": "string",
        "description": "Natural language question about the design",
        "required": True
    }]

    def call(self, params: dict, **kwargs) -> str:
        results, budget_used = retrieve_to_budget(params["query"])  # Module 5
        return format_recall_output(results, budget_used)
```

**The agent loop (what runs the demo):**
```python
from qwen_agent.agents import Assistant

agent = Assistant(
    llm={"model": "qwen3.7-max",
         "api_key": DASHSCOPE_KEY,
         "model_server": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"},
    function_list=["capture_decision", "recall_decisions",
                   "check_invalidation", "supersede_decision"],
    system_message=SYSTEM_PROMPT
)

# Run the demo
for response in agent.run([{"role": "user",
                            "content": "Process this transcript: [Maple Wharf excerpt]"}]):
    print(response)
```

**Time estimate:** 6–10 hours (tool definitions + agent configuration + end-to-end demo test)
**Difficulty:** ★★★☆☆

### Option B · Alternative — OpenAI-style function calling without Qwen-Agent ★★★☆☆

Skip the Qwen-Agent framework entirely. Implement a manual tool-calling loop using the OpenAI-compatible endpoint directly.

```python
# Manual tool loop (simplified)
response = client.chat.completions.create(
    model="qwen3.7-max",
    messages=messages,
    tools=[CAPTURE_TOOL, RECALL_TOOL, INVALIDATION_TOOL]
)

# Check if the model wants to call a tool
if response.choices[0].message.tool_calls:
    for call in response.choices[0].message.tool_calls:
        result = dispatch_tool(call.function.name, call.function.arguments)
        messages.append({"role": "tool", "content": result,
                         "tool_call_id": call.id})
    # Continue the conversation with tool results
```

**Trade-off:** More code to write, but gives you direct control. Easier to debug than Qwen-Agent. Slightly harder to claim "MCP integration" — the judging hook is weaker.

**Recommended if:** Qwen-Agent proves difficult to configure under time pressure.

**Time estimate:** 6–8 hours
**Difficulty:** ★★★☆☆

### Option C · Stretch — MCP server (Model Context Protocol) ★★★★☆

Expose TRACE's tools as a true MCP server that any MCP-compatible client (not just Qwen-Agent) can connect to. This is the "real" MCP integration the judging rubric references.

```python
# TRACE as an MCP server
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("trace")

@server.tool()
async def capture_decision(transcript_chunk: str) -> str:
    """Capture a design decision from AEC transcript text."""
    ...

async def main():
    async with stdio_server() as streams:
        await server.run(*streams, server.create_initialization_options())
```

**Trade-off:** More impressive to judges who understand MCP, but significantly more complex to build and debug. Only attempt this after the `@register_tool` version works.

**Time estimate:** 1–2 days (on top of Option A)
**Difficulty:** ★★★★☆

---

## Module 8 · The Demo Interface

**What it needs to do:** Provide a surface that can be filmed for the ≤3-minute demo video. Must clearly show: (1) transcript ingested → decision captured, (2) red invalidation alert firing, (3) recall with visible context-budget meter, (4) audit trail walking the superseded chain.

### Option A · Recommended — CLI with `rich` library ★★☆☆☆

The `rich` Python library produces beautiful, colourful terminal output — tables, progress bars, panels, coloured text — that photographs well in a screen recording.

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Scene 2: The red alert (the money shot)
console.print(Panel(
    "[bold red]⚠️  TRACE INVALIDATION ALERT[/bold red]\n\n"
    "[white]NEW:[/white]  Facade changed to ACM cladding (D-089)\n"
    "        [dim]J. Park (contractor), 2026-03-15[/dim]\n\n"
    "[white]BREAKS:[/white] D-047 — Facade = terracotta on A2 mineral wool\n"
    "        [dim]Assumption violated: 'combustible cladding prohibited >18m'[/dim]\n\n"
    "[bold yellow]BLAST RADIUS:[/bold yellow]\n"
    "  • Structural: recalculate support brackets\n"
    "  • Fire: cavity barriers require re-specification\n"
    "  • Regulatory: Gateway 2 re-submission required",
    title="[bold red]CONFLICT DETECTED[/bold red]",
    border_style="red"
))
```

**Why this wins for the hackathon:** A rich CLI films excellently, takes 1–2 days to build vs 3–5 for a web UI, and lets you focus time on the actual AI logic rather than frontend code.

**Time estimate:** 4–8 hours
**Difficulty:** ★★☆☆☆

### Option B · Alternative — Thin web UI (FastAPI + HTML/JS) ★★★☆☆

A simple web dashboard that shows:
- A transcript input box (paste text → hit "Process")
- A live decision feed (cards appearing as decisions are captured)
- A big red alert banner when a conflict is detected
- A recall panel with the context-budget progress bar
- An audit trail timeline

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI()
# Serve static HTML/CSS/JS frontend
# WebSocket for live alert push
```

**Trade-off:** Much more polished and impressive on video. Requires 2–3 additional days of frontend work. Only attempt if you have a team member comfortable with HTML/JavaScript.

**Time estimate:** 2–3 days (after CLI version works)
**Difficulty:** ★★★☆☆

### Option C · Stretch — Streamlit dashboard ★★★☆☆

Streamlit lets you build a web UI in pure Python — no HTML/JavaScript required. Faster than a full FastAPI web app, more visual than a CLI.

```python
import streamlit as st

st.title("TRACE — Design Decision Memory Agent")
transcript = st.text_area("Paste meeting transcript:")
if st.button("Process"):
    with st.spinner("Analysing..."):
        result = agent.process_transcript(transcript)
    if result["conflict"]:
        st.error(f"⚠️ CONFLICT: {result['alert']}")
    else:
        st.success(f"✅ Decision captured: {result['decision']['id']}")
```

**Trade-off:** Middle ground between CLI and full web UI. Looks professional with very little frontend effort. The main limitation is Streamlit's opinionated layout — harder to customise the visual design.

**Time estimate:** 4–8 hours (on top of CLI logic)
**Difficulty:** ★★★☆☆

---

## Module 9 · Demo Content — The Maple Wharf Transcripts

**What it needs to do:** Provide the fictional meeting transcripts that drive the demo. These need to tell a three-scene story where Scene 3 inevitably triggers the invalidation alert. The storyline must be deterministic — the alert fires every time.

### Option A · Recommended — Hand-authored fictional transcripts ★☆☆☆☆

Write three short transcript files (~200–400 words each) that tell the Maple Wharf story in a realistic AEC meeting style.

```
transcripts/
├── 01-concept-design-meeting-2026-01-14.txt   # D-047 made (terracotta facade)
├── 02-coordination-review-2026-02-20.txt       # Brief confirmed, no new conflicts
└── 03-value-engineering-2026-03-15.txt         # D-089 proposed (ACM) → ALERT FIRES
```

**Scene 1 transcript sample:**
```
MAPLE WHARF RESIDENTIAL — CONCEPT DESIGN REVIEW
Date: 14 January 2026
Present: R. Wells (Lead Architect), P. Desai (Fire Engineer), S. Chen (Client)

R. Wells: Given the building is 23 metres to the top occupied floor, we are firmly
in higher-risk building territory under the Building Safety Act. P. Desai has
confirmed that Approved Document B Part B4 prohibits any combustible cladding
above 18 metres. We are therefore specifying a terracotta rainscreen system on
A2-s1,d0 mineral wool insulation throughout the facade.

P. Desai: Confirmed. The A2 mineral wool satisfies the non-combustibility
requirement. This is a hard constraint — any future facade change must go back
through fire engineering sign-off and will likely require a Gateway 2 resubmission.

S. Chen: Understood. The terracotta is approved.

DECISION: Facade system confirmed as terracotta rainscreen on A2-s1,d0 mineral
wool insulation. Non-negotiable constraint driven by Building Safety Act 2022
and Approved Document B (B4). Any change requires fire engineering review and
Gateway 2 resubmission. [R. Wells + P. Desai, 14/01/2026]
```

**Why hand-authored beats AI-generated for the demo:**
- You control exactly what decisions are made
- The alert fires deterministically — no surprises during filming
- Realistic AEC language builds credibility with judges who know the industry

**Time estimate:** 3–5 hours (write + refine until extraction quality is good)
**Difficulty:** ★☆☆☆☆

### Option B · Alternative — LLM-generated transcripts (reviewed and edited) ★★☆☆☆

Use an LLM to draft the transcripts, then review and edit them for AEC accuracy. Faster initial draft, but requires careful review to catch hallucinated terminology or unrealistic scenarios.

**Time estimate:** 2–4 hours
**Difficulty:** ★★☆☆☆

---

## Module 10 · Submission Deliverables — Repo, README, Diagram, Video

**What it needs to do:** Produce everything the Devpost submission requires: public GitHub repo with OSS license, architecture diagram, demo video (≤3 min), presentation deck, and written description.

### GitHub Repo ★★☆☆☆
- Set to **public** before submission
- Include `LICENSE` file (MIT is fine, simple, well-recognised)
- `README.md` should cover: what TRACE is, how to install, how to run the demo, architecture overview

**Time estimate:** 2–4 hours (README + license + cleanup)
**Difficulty:** ★★☆☆☆

### Architecture Diagram ★★☆☆☆
- **Option A:** [Excalidraw](https://excalidraw.com/) — free, browser-based, clean hand-drawn aesthetic. Export as PNG. ~2–3 hours.
- **Option B:** [draw.io / diagrams.net](https://draw.io) — free, more formal look. ~2–3 hours.
- **Option C:** Mermaid diagram in the README (code that renders as a diagram on GitHub). ~1 hour. Less visual impact but zero design effort.

**Time estimate:** 2–4 hours
**Difficulty:** ★★☆☆☆

### Demo Video (≤3 minutes) ★★☆☆☆
Three scenes, scripted in advance:
1. **Scene 1 (45 sec):** "A decision is made" — paste Scene 1 transcript → TRACE extracts D-047 → shows the structured record
2. **Scene 2 (75 sec):** "A conflict is detected" — paste Scene 3 transcript → TRACE fires the red alert → explain the blast radius
3. **Scene 3 (45 sec):** "The audit trail" — query "why terracotta?" → TRACE recalls with budget meter → show the superseded chain

**Tools:** OBS Studio (free screen recorder) + DaVinci Resolve (free video editor).

**Time estimate:** 4–8 hours (scripting + recording + editing + upload)
**Difficulty:** ★★☆☆☆

### Presentation Deck ★★☆☆☆
Six slides maximum:
1. The problem (Hackitt quote + BSA 2022)
2. What TRACE does (the four-part loop)
3. The demo (screenshot of the red alert)
4. Architecture diagram
5. Competitive position (the unoccupied square)
6. The team

**Time estimate:** 3–5 hours
**Difficulty:** ★★☆☆☆

---

## Master Timeline — 2–3 Person Team, 12 Days

*Assumes ~8–10 hours/day. `[P]` = can be done in parallel by a second person.*

| Day | Hours | What Gets Built | Module(s) |
|---|---|---|---|
| **Day 1** (Jun 27) | 8h | Repo setup + environment + Qwen API smoke test + Decision schema + SQLite store | 0, 1 |
| **Day 2** (Jun 28) | 8h | `capture_decision` extraction prompt + function-calling + test on Scene 1 transcript `[P]` Write Scene 1 & 2 transcripts | 2, 9 |
| **Day 3** (Jun 29) | 10h | Embeddings + sqlite-vec vector index + hybrid retrieval (dense + BM25) `[P]` Write Scene 3 transcript + rule-pack YAML | 3, 4, 9 |
| **Day 4** (Jun 30) | 10h | LLM premise check + full `check_invalidation` tool + end-to-end test on Maple Wharf (C2 must fire reliably) | 4 |
| **Day 5** (Jul 1) | 10h | Reranking + composite scoring + retrieve-to-budget + context-budget meter + abstention (C3) | 5 |
| **Day 6** (Jul 2) | 8h | Audit trail + history view (C4) `[P]` Architecture diagram draft | 6, 10 |
| **Day 7** (Jul 3) | 10h | Qwen-Agent tool wrapping (C5) — `@register_tool` for all 4 tools + agent loop test | 7 |
| **Day 8** (Jul 4) | 8h | `rich` CLI demo interface + three-scene scripted run-through `[P]` README draft | 8, 10 |
| **Day 9** (Jul 5) | 8h | Full end-to-end rehearsal of three demo scenes — fix any failures `[P]` Presentation deck | All |
| **Day 10** (Jul 6) | 8h | Deploy to Alibaba Cloud (insurance) `[P]` Architecture diagram finalise | 0, 10 |
| **Day 11** (Jul 7–8) | 10h | Record demo video + edit to ≤3 min + upload + written Devpost description | 10 |
| **Day 12** (Jul 9) | 4h | Final checks: repo public + license present + all links working → **SUBMIT before 14:00 PDT** | 10 |

**Critical path:** Day 4 (invalidation alert) is the spine. If Day 4 slips, push Day 5–6 tasks to parallel and protect the alert above all else.

---

## Technology Stack Summary

| Layer | Recommended (Hackathon) | Alternative | Production Path |
|---|---|---|---|
| **Language** | Python 3.11+ | — | Python / TypeScript |
| **Storage** | SQLite + `sqlite-vec` | TinyDB | Neo4j + DashVector |
| **LLM (reasoning)** | `qwen3.7-max` | `qwen-plus` | `qwen3.7-max` |
| **LLM (extraction)** | `qwen-plus` / `qwen-flash` | `qwen3.7-max` | fine-tuned Qwen |
| **Embeddings** | `text-embedding-v4` 1024d | `text-embedding-v3` | `text-embedding-v4` 2048d |
| **Reranking** | `qwen3-rerank` | `gte-rerank-v2` | `qwen3-rerank` |
| **Keyword search** | `rank-bm25` (Python) | manual TF-IDF | Elasticsearch |
| **Agent framework** | Qwen-Agent `@register_tool` | manual tool loop | MCP server |
| **Rule-pack** | YAML + Python checker | hardcoded Python | DSL + rules engine |
| **Demo interface** | `rich` CLI | Streamlit | FastAPI web app |
| **Architecture diagram** | Excalidraw | draw.io | — |
| **Video** | OBS + DaVinci Resolve | Loom | — |
| **Deployment** | Alibaba Cloud ECS (insurance) | — | Alibaba Cloud |

---

## Quick-Start Checklist (Day 1)

- [ ] Create GitHub repo, set to **public**, add MIT `LICENSE` file
- [ ] Python 3.11+ installed (`python --version`)
- [ ] `pip install openai python-dotenv pyyaml sqlite-vec rank-bm25 rich`
- [ ] Create `.env` with `DASHSCOPE_API_KEY=your_key_here`
- [ ] Verify Qwen API works: call `qwen-plus` with a test message on the Singapore endpoint
- [ ] Create `decisions` table in SQLite; insert one dummy Decision row; read it back
- [ ] Paste Scene 1 transcript excerpt; confirm extraction returns a valid JSON Decision

When all seven boxes are ticked, the spine exists. Everything else is building on top of it.

---

*Cross-references: [02 · Architecture](02-architecture.md) for the pipeline design · [03 · Strategy](03-hackathon-strategy.md) for the build-order priorities · [04 · Qwen Tech Reference](04-qwen-tech-reference.md) for model IDs and API details · [06 · Open Questions](06-open-questions.md) for unresolved decisions.*
