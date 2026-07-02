"""Offline replay for the demo — the no-key / no-network safety net.

`python cli.py --offline` replays canned Qwen responses from demo_replay.json,
so the demo runs on a fresh clone with no API key and can never fail on camera.
`python cli.py --record` runs the demo live AND refreshes the fixture from the
real Qwen responses, so the canned run stays authentic.

The fixture is an ordered list of the responses the demo consumes (the demo's
LLM call sequence is deterministic): capture ×2, court roles ×3, recall ×1.
Entry kinds: {"kind": "tool_calls", "calls": [{name, arguments}]} for
function-calling responses, {"kind": "content", "text": "..."} for text.
"""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

FIXTURE = Path(__file__).with_name("demo_replay.json")


def _to_response(entry: dict) -> SimpleNamespace:
    if entry["kind"] == "tool_calls":
        tcs = [
            SimpleNamespace(function=SimpleNamespace(
                name=c["name"], arguments=json.dumps(c["arguments"])))
            for c in entry["calls"]
        ]
        msg = SimpleNamespace(content=None, tool_calls=tcs)
    else:
        msg = SimpleNamespace(content=entry["text"], tool_calls=None)
    return SimpleNamespace(choices=[SimpleNamespace(message=msg)])


class ReplayClient:
    """OpenAI-compatible client that replays the fixture in order. No network."""

    def __init__(self, path=FIXTURE):
        self._queue = list(json.loads(Path(path).read_text(encoding="utf-8")))
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **_kw):
        if not self._queue:
            raise RuntimeError(
                "Replay fixture exhausted — the demo made more LLM calls than the "
                "fixture holds. Refresh it with: python cli.py --record"
            )
        return _to_response(self._queue.pop(0))


class RecordingClient:
    """Wraps a real client; saves every response to the fixture as it streams by."""

    def __init__(self, real, path=FIXTURE):
        self._real, self._path, self._log = real, Path(path), []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kw):
        resp = self._real.chat.completions.create(**kw)
        msg = resp.choices[0].message
        if getattr(msg, "tool_calls", None):
            self._log.append({"kind": "tool_calls", "calls": [
                {"name": tc.function.name, "arguments": json.loads(tc.function.arguments)}
                for tc in msg.tool_calls
            ]})
        else:
            self._log.append({"kind": "content", "text": msg.content})
        self._path.write_text(json.dumps(self._log, indent=1), encoding="utf-8")
        return resp
