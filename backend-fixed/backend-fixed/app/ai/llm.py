"""
AI Boardroom — LLM Wrapper
Configures and provides the core language models.
"""

from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


def get_llm(model_name: str = "gemini-2.0-flash", temperature: float = 0.2) -> ChatGoogleGenerativeAI:
    """Instantiate a ChatGoogleGenerativeAI model with project settings."""
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        google_api_key=settings.GEMINI_API_KEY,
        model=model_name,
        temperature=temperature,
        max_tokens=4000,
    )


def get_fast_llm() -> ChatGoogleGenerativeAI:
    """Instantiate a faster, cheaper model for simple tasks."""
    return get_llm(model_name="gemini-1.5-flash", temperature=0.1)


def get_reasoning_llm() -> ChatGoogleGenerativeAI:
    """Instantiate a high-reasoning model for complex analysis."""
    # Assuming standard gemini-2.5-pro for now
    return get_llm(model_name="gemini-2.5-pro", temperature=0.3)
