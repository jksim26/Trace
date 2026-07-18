"""The vault watcher's polling loop — the intake path test_kb.py only touches
once. Under test here: mtime dedupe across polls, re-ingest on modification
(content-addressed, so a mere re-save is a no-op), the loop-guards (Trace
projections and wrong-project notes never enter the record), frontmatter
handling through the loop, and the persistent store the loop opens by default.
All offline: fake clients, temp dirs, bounded polls."""
import json
from types import SimpleNamespace

import pytest

from scenarios import open_store
from store import connect, get_all_decisions, get_decision, init_db
from vault_watcher import ingest_note, watch


def _tool_call(args: dict):
    return SimpleNamespace(function=SimpleNamespace(arguments=json.dumps(args)))


def _counting_capture_client(decisions: list[dict]):
    """Every create() call returns the same record_decision tool-calls, and the
    client counts its calls — the probe for 'did the loop re-capture?'."""
    client = SimpleNamespace(calls=0)

    def create(**kw):
        client.calls += 1
        msg = SimpleNamespace(content="", tool_calls=[_tool_call(a) for a in decisions])
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])
    client.chat = SimpleNamespace(completions=SimpleNamespace(create=create))
    return client


DECISION = [{"statement": "Repair the lobby soffit", "discipline": "architecture",
             "rationale": "leak", "assumptions": ["scope agreed"], "author": ["K. Lim"]}]


def _fresh():
    conn = connect(":memory:")
    init_db(conn)
    return conn


def _inbox(tmp_path, project="tanglin-rise"):
    inbox = tmp_path / project / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    return inbox


# ── the polling loop ─────────────────────────────────────────────────────────

def test_watch_reads_an_unchanged_file_only_once_across_polls(tmp_path):
    conn = _fresh()
    (_inbox(tmp_path) / "meeting.md").write_text("## Meeting\nFix the soffit.\n",
                                                 encoding="utf-8")
    client = _counting_capture_client(DECISION)
    watch("tanglin-rise", conn=conn, root=tmp_path, client=client, max_polls=3, poll=0)
    assert client.calls == 1                      # polled 3×, captured once (mtime dedupe)
    assert len(get_all_decisions(conn)) == 1


def test_watch_rerun_on_identical_content_is_a_noop(tmp_path):
    # A watcher restart re-reads every inbox file (fresh mtime cache) — the
    # content-addressed episode dedupe must make that a no-op, not a re-capture.
    conn = _fresh()
    (_inbox(tmp_path) / "meeting.md").write_text("## Meeting\nFix the soffit.\n",
                                                 encoding="utf-8")
    watch("tanglin-rise", conn=conn, root=tmp_path,
          client=_counting_capture_client(DECISION), max_polls=1)
    rerun_client = _counting_capture_client(DECISION)
    watch("tanglin-rise", conn=conn, root=tmp_path, client=rerun_client, max_polls=1)
    assert rerun_client.calls == 0                # duplicate episode: no LLM call at all
    assert len(get_all_decisions(conn)) == 1


def test_watch_reingests_a_note_whose_content_changed(tmp_path):
    conn = _fresh()
    note = _inbox(tmp_path) / "meeting.md"
    note.write_text("## Meeting\nFix the soffit.\n", encoding="utf-8")
    watch("tanglin-rise", conn=conn, root=tmp_path,
          client=_counting_capture_client(DECISION), max_polls=1)
    note.write_text("## Meeting (rev B)\nFix the soffit AND the canopy.\n",
                    encoding="utf-8")
    watch("tanglin-rise", conn=conn, root=tmp_path,
          client=_counting_capture_client(DECISION), max_polls=1)
    episodes = conn.execute("SELECT COUNT(*) AS n FROM episodes").fetchone()["n"]
    assert episodes == 2                          # both versions on the record
    assert len(get_all_decisions(conn)) == 2


def test_watch_ingests_every_note_found_in_one_poll(tmp_path):
    conn = _fresh()
    inbox = _inbox(tmp_path)
    (inbox / "a.md").write_text("## Meeting A\nSoffit repair agreed.\n", encoding="utf-8")
    (inbox / "b.md").write_text("## Meeting B\nCanopy repair agreed.\n", encoding="utf-8")
    watch("tanglin-rise", conn=conn, root=tmp_path,
          client=_counting_capture_client(DECISION), max_polls=1)
    episodes = conn.execute("SELECT COUNT(*) AS n FROM episodes").fetchone()["n"]
    assert episodes == 2


def test_watch_never_ingests_a_trace_projection_from_the_inbox(tmp_path):
    # The loop-guard that keeps sources and projections one-way: our own
    # generated note dropped (or misfiled) into the inbox must never re-enter.
    conn = _fresh()
    (_inbox(tmp_path) / "stray.md").write_text(
        '---\ngenerated-by: "trace"\nid: "D-001"\n---\n# D-001 — x\n', encoding="utf-8")
    client = _counting_capture_client(DECISION)
    watch("tanglin-rise", conn=conn, root=tmp_path, client=client, max_polls=1)
    assert client.calls == 0
    assert conn.execute("SELECT COUNT(*) AS n FROM episodes").fetchone()["n"] == 0


def test_watch_skips_a_note_addressed_to_another_project(tmp_path):
    conn = _fresh()
    (_inbox(tmp_path) / "wrong.md").write_text(
        "---\nproject: kranji-hub\n---\nMeeting note.\n", encoding="utf-8")
    client = _counting_capture_client(DECISION)
    watch("tanglin-rise", conn=conn, root=tmp_path, client=client, max_polls=1)
    assert client.calls == 0
    assert conn.execute("SELECT COUNT(*) AS n FROM episodes").fetchone()["n"] == 0


def test_watch_unknown_project_refuses_to_start(tmp_path):
    with pytest.raises(SystemExit):
        watch("no-such-project", root=tmp_path, max_polls=1)


def test_watch_applies_the_notes_date_as_valid_from(tmp_path):
    # Bi-temporal honesty through the LOOP: the note's own date is when the
    # decision became true in the world; ingest time is when Trace learned it.
    conn = _fresh()
    (_inbox(tmp_path) / "meeting.md").write_text(
        "---\ndate: 2026-02-01\n---\n## Meeting\nFix the soffit.\n", encoding="utf-8")
    watch("tanglin-rise", conn=conn, root=tmp_path,
          client=_counting_capture_client(DECISION), max_polls=1)
    d = get_all_decisions(conn)[0]
    assert d.valid_from == "2026-02-01T00:00:00Z"
    assert d.recorded_at != d.valid_from          # learned later than it was decided


def test_watch_stores_a_decisionless_meeting_as_an_episode_only(tmp_path):
    conn = _fresh()
    (_inbox(tmp_path) / "minutes.md").write_text(
        "## Meeting\nOpen discussion only; nothing agreed.\n", encoding="utf-8")
    watch("tanglin-rise", conn=conn, root=tmp_path,
          client=_counting_capture_client([]), max_polls=1)
    assert conn.execute("SELECT COUNT(*) AS n FROM episodes").fetchone()["n"] == 1
    assert get_all_decisions(conn) == []          # no invented decisions


def test_watch_defaults_to_the_shared_persistent_store(tmp_path):
    # Run the loop with NO conn: it must open kb-root/<project>/trace.db (the
    # same file the bubble and MCP server read) — and the ingest must be
    # visible through a second, independent connection to that file.
    (_inbox(tmp_path) / "meeting.md").write_text("## Meeting\nFix the soffit.\n",
                                                 encoding="utf-8")
    watch("tanglin-rise", root=tmp_path,
          client=_counting_capture_client(DECISION), max_polls=1)
    reader = open_store("tanglin-rise", root=tmp_path)
    new = [d for d in get_all_decisions(reader) if d.statement == "Repair the lobby soffit"]
    assert len(new) == 1
    assert get_decision(reader, new[0].id).source_episode  # provenance intact


# ── ingest_note edges the loop relies on ─────────────────────────────────────

def test_ingest_note_tolerates_non_dict_frontmatter():
    conn = _fresh()
    out = ingest_note(conn, "---\n- just\n- a list\n---\nBody.\n",
                      client=_counting_capture_client([]))
    assert out is not None and out["captured"] == []
    assert conn.execute("SELECT COUNT(*) AS n FROM episodes").fetchone()["n"] == 1
