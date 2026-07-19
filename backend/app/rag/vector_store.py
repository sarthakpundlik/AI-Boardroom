"""
AI Boardroom — Vector Store
Qdrant database operations for the RAG pipeline.
"""

from __future__ import annotations

import uuid

from qdrant_client.http.models import Filter, PointStruct, Record

from app.core.config import get_settings
from app.core.constants import TOP_K_RETRIEVAL
from app.database.qdrant import get_qdrant_client
from app.rag.embeddings import embed_texts


class VectorStore:
    """Manages document chunks in Qdrant."""

    def __init__(self, collection_name: str | None = None) -> None:
        self.settings = get_settings()
        self.client = get_qdrant_client()
        self.collection_name = collection_name or self.settings.QDRANT_COLLECTION_NAME

    async def add_texts(
        self, texts: list[str], metadatas: list[dict] | None = None
    ) -> list[str]:
        """Embed and store texts with optional metadata."""
        if not texts:
            return []

        embeddings = await embed_texts(texts)
        ids = [str(uuid.uuid4()) for _ in texts]
        
        points = []
        for i, text in enumerate(texts):
            payload = metadatas[i] if metadatas else {}
            payload["page_content"] = text
            points.append(
                PointStruct(id=ids[i], vector=embeddings[i], payload=payload)
            )

        # Qdrant client is sync, use run_in_threadpool in production
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )
        return ids

    def search(
        self, query_vector: list[float], limit: int = TOP_K_RETRIEVAL, query_filter: Filter | None = None
    ) -> list[Record]:
        """Search for similar vectors."""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
        )
        return results
