"""
AI Boardroom — Retriever
Semantic search and context retrieval.
"""

from __future__ import annotations

from qdrant_client.http.models import FieldCondition, Filter, MatchValue

from app.core.constants import TOP_K_RETRIEVAL
from app.rag.embeddings import embed_query
from app.rag.vector_store import VectorStore


class Retriever:
    """Retrieves relevant context for agents."""

    def __init__(self) -> None:
        self.vector_store = VectorStore()

    async def retrieve_for_project(self, query: str, project_id: str, limit: int = TOP_K_RETRIEVAL) -> list[dict]:
        """Retrieve relevant chunks scoped to a specific project."""
        query_vector = await embed_query(query)
        
        # Filter by project_id
        qdrant_filter = Filter(
            must=[
                FieldCondition(
                    key="project_id", match=MatchValue(value=project_id)
                )
            ]
        )
        
        results = self.vector_store.search(
            query_vector=query_vector,
            limit=limit,
            query_filter=qdrant_filter,
        )
        
        # Format results
        return [
            {
                "content": hit.payload.get("page_content", ""),
                "metadata": hit.payload,
                "score": hit.score,
            }
            for hit in results
        ]
