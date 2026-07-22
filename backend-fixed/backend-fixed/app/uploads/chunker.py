"""
AI Boardroom — Text Chunker
Chunks extracted text for the RAG pipeline.
"""

from __future__ import annotations

from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.core.constants import CHUNK_OVERLAP, CHUNK_SIZE


def chunk_text(text: str) -> list[str]:
    """Split text into overlapping chunks suitable for embedding."""
    if not text:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
        length_function=len,
    )
    
    return text_splitter.split_text(text)
