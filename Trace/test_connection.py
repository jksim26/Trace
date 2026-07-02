"""Live Qwen Cloud smoke test — the only test that needs a network + API key.

Skipped automatically when DASHSCOPE_API_KEY is not set, so a bare
`python -m pytest` on a fresh clone collects and passes offline.
"""
import os

import pytest
from dotenv import load_dotenv

load_dotenv()

pytestmark = pytest.mark.skipif(
    not os.getenv("DASHSCOPE_API_KEY"),
    reason="live API smoke test — set DASHSCOPE_API_KEY in Trace/.env to run",
)


def test_qwen_connection():
    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": "Reply with exactly: TRACE connection successful."}],
    )
    assert "TRACE connection successful" in response.choices[0].message.content
