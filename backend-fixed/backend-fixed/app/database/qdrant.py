"""
AI Boardroom — Qdrant Vector Store Client
Manages connections and collections for the Qdrant vector database.
"""

from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.core.config import get_settings
from app.core.constants import EMBEDDING_DIMENSION
from app.core.logging import get_logger

logger = get_logger(__name__)

_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    """Get or create the Qdrant client singleton."""
    global _client
    if _client is None:
        settings = get_settings()
        _client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            api_key=settings.QDRANT_API_KEY or None,
        )
        logger.info(
            "Qdrant client initialized",
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
    return _client


async def init_qdrant_collections() -> None:
    """Create required Qdrant collections if they don't exist."""
    client = get_qdrant_client()
    settings = get_settings()

    collections = {
        settings.QDRANT_COLLECTION_NAME: EMBEDDING_DIMENSION,
        "session_memory": EMBEDDING_DIMENSION,
        "agent_memory": EMBEDDING_DIMENSION,
    }

    existing = {c.name for c in client.get_collections().collections}

    for name, dimension in collections.items():
        if name not in existing:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=dimension,
                    distance=Distance.COSINE,
                ),
            )
            logger.info("Created Qdrant collection", collection=name, dimension=dimension)
        else:
            logger.info("Qdrant collection already exists", collection=name)


def close_qdrant() -> None:
    """Close the Qdrant client connection."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
        logger.info("Qdrant client closed")
