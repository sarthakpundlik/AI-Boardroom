"""
AI Boardroom — Embeddings
Generates vector embeddings for text chunks.
"""

from __future__ import annotations

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import get_settings


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """Get the Gemini embeddings model."""
    settings = get_settings()
    return GoogleGenerativeAIEmbeddings(
        google_api_key=settings.GEMINI_API_KEY,
        model="models/text-embedding-004",
    )


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of text strings."""
    if not texts:
        return []
    model = get_embedding_model()
    # Await is needed if using async methods, but langchain_openai aembed_documents is available
    return await model.aembed_documents(texts)


async def embed_query(text: str) -> list[float]:
    """Embed a single query string."""
    if not text:
        return []
    model = get_embedding_model()
    return await model.aembed_query(text)
