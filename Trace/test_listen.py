import json
from types import SimpleNamespace

import pytest

from listen import listen_and_capture, record_from_mic, transcribe_audio


def _fake_transcribe_client(text="The facade cladding shall be non-combustible."):
    create = lambda **kw: SimpleNamespace(text=text)
    return SimpleNamespace(audio=SimpleNamespace(transcriptions=SimpleNamespace(create=create)))


def _fake_tc(args: dict):
    return SimpleNamespace(function=SimpleNamespace(name="record_decision", arguments=json.dumps(args)))


def _fake_capture_client(decisions):
    tcs = [_fake_tc(d) for d in decisions]
    create = lambda **kw: SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(tool_calls=tcs))]
    )
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def test_transcribe_audio_returns_the_text(tmp_path):
    audio = tmp_path / "meeting.wav"
    audio.write_bytes(b"not real audio, just needs to exist and be openable")
    text = transcribe_audio(str(audio), client=_fake_transcribe_client("hello from the meeting"))
    assert text == "hello from the meeting"


def test_listen_and_capture_runs_the_full_pipeline(tmp_path):
    audio = tmp_path / "01-concept-design.wav"
    audio.write_bytes(b"not real audio, just needs to exist and be openable")
    decisions = [{
        "statement": "Facade cladding = non-combustible mineral rainscreen",
        "discipline": "facade",
        "rationale": "SCDF Cl 3.5 requires non-combustible external wall over 15 m",
        "assumptions": ["building exceeds 15 m"],
        "author": ["K. Lim"],
    }]
    result = listen_and_capture(
        str(audio),
        transcribe_client=_fake_transcribe_client("We agreed on non-combustible cladding."),
        capture_client=_fake_capture_client(decisions),
    )
    assert result.transcript == "We agreed on non-combustible cladding."
    assert len(result.captured) == 1
    c = result.captured[0]
    assert c.decision.statement == "Facade cladding = non-combustible mineral rainscreen"
    assert c.decision.discipline == "facade"
    # source_episode defaults to the audio file's stem when not given explicitly
    assert c.decision.source_episode == "01-concept-design"


def test_listen_and_capture_honours_explicit_source_episode(tmp_path):
    audio = tmp_path / "recording.wav"
    audio.write_bytes(b"placeholder")
    result = listen_and_capture(
        str(audio), source_episode="site-meeting-2026-03-03",
        transcribe_client=_fake_transcribe_client("no decisions here"),
        capture_client=_fake_capture_client([]),
    )
    assert result.captured == []


def test_record_from_mic_raises_helpfully_when_dependency_missing(monkeypatch):
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "sounddevice":
            raise ImportError("no module named sounddevice")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(RuntimeError, match="sounddevice"):
        record_from_mic(1.0)
