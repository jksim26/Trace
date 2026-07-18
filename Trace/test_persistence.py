"""The shared persistent store (open_store): one on-disk trace.db per project
that the vault watcher, the bubble chat and the MCP server all open — so an
ingested note reaches every surface, and nothing is lost on restart. These
tests run offline (fake clients, temp dirs)."""
import json
from types import SimpleNamespace

import pytest

import bubble
import mcp_server
from scenarios import open_store
from store import Decision, add_decision, get_all_decisions, get_decision
from vault_watcher import ingest_note


def _tool_call(args: dict):
    return SimpleNamespace(function=SimpleNamespace(arguments=json.dumps(args)))


def _capture_client(decisions: list[dict]):
    def create(**kw):
        msg = SimpleNamespace(content="", tool_calls=[_tool_call(a) for a in decisions])
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


NOTE = "## Site meeting\nWe will repair the lobby soffit.\n"
CAPTURED = [{"statement": "Repair the lobby soffit", "discipline": "architecture",
             "rationale": "leak", "assumptions": ["scope agreed"], "author": ["K. Lim"]}]


def test_open_store_seeds_the_demo_scenario_on_first_open(tmp_path):
    conn = open_store("tanglin-rise", root=tmp_path)
    assert (tmp_path / "tanglin-rise" / "trace.db").is_file()
    ids = {d.id for d in get_all_decisions(conn)}
    assert "408213-D-001" in ids and "408213-D-006" in ids  # the full demo seed


def test_open_store_persists_across_connections_and_never_reseeds(tmp_path):
    conn = open_store("tanglin-rise", root=tmp_path)
    n_seeded = len(get_all_decisions(conn))
    add_decision(conn, Decision(statement="Lobby ceiling = acoustic timber slats"))
    conn.close()
    reopened = open_store("tanglin-rise", root=tmp_path)  # restart survives
    ds = get_all_decisions(reopened)
    assert len(ds) == n_seeded + 1                        # kept, not re-seeded
    assert len({d.id for d in ds}) == len(ds)             # no duplicate demo rows


def test_open_store_treats_an_empty_file_as_fresh(tmp_path):
    db = tmp_path / "tanglin-rise" / "trace.db"
    db.parent.mkdir(parents=True)
    db.touch()  # e.g. an aborted copy
    conn = open_store("tanglin-rise", root=tmp_path)
    assert get_all_decisions(conn)


def test_open_store_unknown_project_raises_keyerror(tmp_path):
    with pytest.raises(KeyError):
        open_store("no-such-project", root=tmp_path)


def test_two_connections_share_one_record(tmp_path):
    # The watcher's connection and the bubble's connection are different
    # objects on the SAME file: a write through one is read by the other.
    writer = open_store("tanglin-rise", root=tmp_path)
    reader = open_store("tanglin-rise", root=tmp_path)
    out = ingest_note(writer, NOTE, path="inbox/meeting.md",
                      client=_capture_client(CAPTURED))
    new_id = out["captured"][0]["id"]
    seen = get_decision(reader, new_id)
    assert seen is not None and seen.statement == "Repair the lobby soffit"
    assert seen.source_episode == out["episode"]


def test_bubble_chat_sees_a_watcher_ingested_note(tmp_path, monkeypatch):
    # The story on the tin: drop a note in the inbox, then ask the bubble about
    # it — both sides open kb/<project>/trace.db, so the answer includes it.
    monkeypatch.setenv("TRACE_DB_DIR", str(tmp_path))
    monkeypatch.setattr(bubble, "_STORES", {})
    monkeypatch.setattr(bubble, "_apis", {})
    watcher_conn = open_store("tanglin-rise", root=tmp_path)
    out = ingest_note(watcher_conn, NOTE, client=_capture_client(CAPTURED))
    state = json.loads(bubble.Api("tanglin-rise").state())
    assert out["captured"][0]["id"] in {d["id"] for d in state["decisions"]}


def test_mcp_server_sees_a_watcher_ingested_note(tmp_path, monkeypatch):
    monkeypatch.setenv("TRACE_DB_DIR", str(tmp_path))
    monkeypatch.setattr(mcp_server, "_STORES", {})
    watcher_conn = open_store("tanglin-rise", root=tmp_path)
    out = ingest_note(watcher_conn, NOTE, client=_capture_client(CAPTURED))
    listed = mcp_server.list_decisions("tanglin-rise")
    assert out["captured"][0]["id"] in {d["id"] for d in listed["decisions"]}
