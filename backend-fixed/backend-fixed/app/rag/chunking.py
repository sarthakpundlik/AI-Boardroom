"""
AI Boardroom — RAG Chunking
Logical wrapper for chunking within the RAG pipeline.
"""

from __future__ import annotations

from app.uploads.chunker import chunk_text


def prepare_chunks_for_rag(text: str, metadata: dict) -> tuple[list[str], list[dict]]:
    """Split text and duplicate metadata for each chunk."""
    chunks = chunk_text(text)
    metadatas = [metadata.copy() for _ in chunks]
    return chunks, metadatas
