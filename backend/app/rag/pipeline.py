"""
AI Boardroom — RAG Pipeline
End-to-end RAG orchestration.
"""

from __future__ import annotations

from app.rag.chunking import prepare_chunks_for_rag
from app.rag.context import build_agent_context
from app.rag.reranker import rerank_documents
from app.rag.retriever import Retriever
from app.rag.vector_store import VectorStore


class RAGPipeline:
    """Orchestrates ingestion and retrieval for RAG."""

    def __init__(self) -> None:
        self.vector_store = VectorStore()
        self.retriever = Retriever()

    async def ingest_document(self, text: str, document_id: str, project_id: str, filename: str) -> int:
        """Process and store a document in the vector DB."""
        metadata = {
            "document_id": document_id,
            "project_id": project_id,
            "filename": filename,
        }
        
        chunks, metadatas = prepare_chunks_for_rag(text, metadata)
        
        if not chunks:
            return 0
            
        await self.vector_store.add_texts(chunks, metadatas)
        return len(chunks)

    async def get_context(self, query: str, project_id: str) -> str:
        """Retrieve, rerank, and format context for an agent query."""
        # 1. Retrieve
        raw_docs = await self.retriever.retrieve_for_project(query, project_id)
        
        # 2. Rerank
        ranked_docs = rerank_documents(query, raw_docs)
        
        # 3. Format
        context_str = build_agent_context(ranked_docs)
        
        return context_str
