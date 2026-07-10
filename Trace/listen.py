"""C0 — listen: the missing first mile. Turns a recorded meeting into the
same plain-text transcript capture_decision() already expects, so nothing
downstream (store, invalidate, court, recall) has to change.

Two ways in:
  1. transcribe_audio(path)   — an existing audio file (wav/mp3/m4a/ogg/...)
  2. record_from_mic(seconds) — record straight from a microphone (optional
                                 dependency: `pip install sounddevice`)

Uses the same Qwen Cloud (DashScope) client + key as the rest of Trace
(DASHSCOPE_API_KEY) — no separate account or transcription service to set up.

[web search, unverified] TRANSCRIBE_MODEL below is Alibaba's Qwen3-ASR,
which DashScope documents as reachable through the standard OpenAI
`client.audio.transcriptions.create(file=..., model=...)` shape (the same
shape this module calls). I could not load Alibaba's live API-reference page
from this sandbox (it 403'd every fetch attempt), so the exact model string
and whether it needs a different base_url than the rest of Trace's chat
calls is NOT independently confirmed — check it against your own DashScope
console (or just try one real call and read the error, which lists valid
model names) before relying on this for a live demo. Everything else in this
module (the transcribe -> capture pipeline, the mic recorder, the CLI) does
not depend on that string being exactly right.
"""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from capture import Captured, capture_decision

load_dotenv()

TRANSCRIBE_MODEL = "qwen3-asr-flash"  # [web search, unverified] — see module docstring
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=BASE_URL)


def transcribe_audio(path: str, client=None, model: str = TRANSCRIBE_MODEL) -> str:
    """Turn a recorded audio file into plain text — the exact shape
    capture_decision() already reads. `path` can be any format the
    transcription model accepts (wav/mp3/m4a/ogg/... — a local file, not a
    public URL)."""
    client = client or _client()
    with open(path, "rb") as f:
        resp = client.audio.transcriptions.create(model=model, file=f)
    return resp.text


@dataclass
class ListenResult:
    transcript: str
    captured: list[Captured]


def listen_and_capture(path: str, *, source_episode: str = "", recorded_at=None,
                       valid_from=None, transcribe_client=None, capture_client=None,
                       transcribe_model: str = TRANSCRIBE_MODEL) -> ListenResult:
    """The missing first mile, end to end: audio file -> transcript ->
    Captured decisions, running through the exact same capture_decision()
    every other Trace path already uses. The caller adds the results to a
    store (and runs invalidation/the court) exactly as it would for a typed
    transcript — this module only produces the same Captured list capture.py
    already produces, from audio instead of typed text."""
    transcript = transcribe_audio(path, client=transcribe_client, model=transcribe_model)
    captured = capture_decision(
        transcript, source_episode=source_episode or Path(path).stem,
        recorded_at=recorded_at, valid_from=valid_from, client=capture_client,
    )
    return ListenResult(transcript=transcript, captured=captured)


def record_from_mic(seconds: float, out_path: Optional[str] = None,
                    samplerate: int = 16000) -> str:
    """Record `seconds` of audio from the default microphone to a wav file
    and return its path. Needs the OPTIONAL `sounddevice` package (PortAudio)
    — not in requirements.txt, since nothing else in Trace needs it and
    PortAudio can be finicky to install on some machines:
        pip install sounddevice
    Everything else in this module works on any audio file you already have,
    recorded however you like (a phone, a meeting app's own recorder, etc.)."""
    try:
        import sounddevice as sd
        import soundfile as sf
    except ImportError as e:
        raise RuntimeError(
            "Microphone recording needs the optional 'sounddevice' package "
            "(pip install sounddevice) — everything else in listen.py works "
            "without it if you already have an audio file."
        ) from e
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype="float32")
    sd.wait()
    out_path = out_path or tempfile.mktemp(suffix=".wav")
    sf.write(out_path, audio, samplerate)
    return out_path


def _cli() -> None:
    import sys
    if len(sys.argv) < 2:
        print("Usage:\n  python listen.py <audio-file>\n  python listen.py --record <seconds>")
        return
    if sys.argv[1] == "--record":
        seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
        print(f"Recording {seconds:.0f}s from the microphone... (Ctrl+C to cancel)")
        path = record_from_mic(seconds)
    else:
        path = sys.argv[1]
    result = listen_and_capture(path)
    print(f"\nTranscript:\n{result.transcript}\n")
    if not result.captured:
        print("No decisions detected in this recording.")
        return
    for c in result.captured:
        print(f"Captured: {c.decision.statement}")
        print(f"  WHY: {c.decision.rationale}")
        if c.decision.assumptions:
            print(f"  ASSUMES: {'; '.join(c.decision.assumptions)}")


if __name__ == "__main__":
    _cli()
