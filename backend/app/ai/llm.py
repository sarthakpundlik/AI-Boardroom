"""
AI Boardroom — LLM Wrapper
Configures and provides the core language models.
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from app.core.config import get_settings


def get_llm(model_name: str = "gpt-4o", temperature: float = 0.2) -> ChatOpenAI:
    """Instantiate a ChatOpenAI model with project settings."""
    settings = get_settings()
    return ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model=model_name,
        temperature=temperature,
        max_tokens=4000,
    )


def get_fast_llm() -> ChatOpenAI:
    """Instantiate a faster, cheaper model for simple tasks."""
    return get_llm(model_name="gpt-4o-mini", temperature=0.1)


def get_reasoning_llm() -> ChatOpenAI:
    """Instantiate a high-reasoning model for complex analysis."""
    # Assuming standard gpt-4o for now, could be o1 if available via langchain
    return get_llm(model_name="gpt-4o", temperature=0.3)
