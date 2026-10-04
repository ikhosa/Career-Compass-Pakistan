from __future__ import annotations

import os
from typing import Optional

from crewai import LLM


MODEL_NAME = "groq/openai/gpt-oss-120b"


def get_api_key() -> Optional[str]:
    key = os.getenv("GROQ_API_KEY", "").strip()
    return key or None


def require_api_key() -> str:
    key = get_api_key()
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to Streamlit Secrets before running the app."
        )
    return key


def get_llm() -> LLM:
    """Return the single Grok configuration used by all four agents."""
    return LLM(
        model=MODEL_NAME,
        api_key=require_api_key(),
        timeout=120,
        max_tokens=1800,
    )
