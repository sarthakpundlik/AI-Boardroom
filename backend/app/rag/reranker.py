"""
AI Boardroom — Reranker
Optional post-retrieval reranking of chunks.
"""

from __future__ import annotations

# In a full implementation, you might use Cohere or a local CrossEncoder here.
# For now, we return the documents as-is (they are already sorted by Cosine distance from Qdrant).

def rerank_documents(query: str, documents: list[dict], top_n: int = 5) -> list[dict]:
    """
    Rerank documents to improve precision.
    Currently a pass-through.
    """
    return documents[:top_n]
