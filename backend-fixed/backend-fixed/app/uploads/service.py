"""
AI Boardroom — Upload Service
Business logic for handling file uploads and triggering processing.
"""

from __future__ import annotations

import asyncio

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.projects.service import ProjectService
from app.uploads.extractor import extract_text
from app.uploads.models import Document
from app.uploads.parser import parse_structured_data
from app.uploads.repository import DocumentRepository
from app.uploads.uploader import Uploader

logger = get_logger(__name__)


class UploadService:
    """Service layer for document uploads."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = DocumentRepository(session)
        self.project_service = ProjectService(session)
        self.uploader = Uploader()

    async def upload_document(self, project_id: str, user_id: str, file: UploadFile) -> Document:
        """Process an uploaded file for a project."""
        # 1. Verify project ownership
        await self.project_service.get_project(project_id, user_id)

        # 2. Upload file via Uploader (validates & saves to storage)
        storage_path, mime_type, file_size, content = await self.uploader.handle_upload(file, project_id)

        # 3. Create Document DB record
        doc = Document(
            project_id=project_id,
            user_id=user_id,
            filename=file.filename or "unknown",
            mime_type=mime_type,
            file_size_bytes=file_size,
            storage_path=storage_path,
            status="pending",
        )
        doc = await self.repo.create(doc)

        # 4. In a real production system, dispatch a Celery task here to process the file.
        # For simplicity in this structure, we'll trigger an async background task.
        asyncio.create_task(self._process_document(doc.id, content, mime_type, file.filename or ""))

        return doc

    async def _process_document(self, document_id: str, content: bytes, mime_type: str, filename: str) -> None:
        """Background task to extract text and trigger RAG pipeline chunking."""
        try:
            # Re-fetch document in new session context (or use passed ID)
            # In Celery this would use a new DB session.
            logger.info("Processing document", document_id=document_id)
            
            # Extract text
            text = extract_text(content, mime_type, filename)
            
            if not text:
                # Might be structured data
                data = parse_structured_data(content, mime_type, filename)
                text = str(data)
                
            # Here we would send text to the RAG pipeline (Phase 6)
            # e.g., chunks = chunk_text(text)
            # embed_and_store(chunks, document_id, project_id)
            
            # Mark as processed
            await self.repo.update_status(document_id, "processed")
            logger.info("Document processed successfully", document_id=document_id)
            
        except Exception as e:
            logger.error("Document processing failed", document_id=document_id, error=str(e))
            await self.repo.update_status(document_id, "failed", str(e))

    async def list_documents(self, project_id: str, user_id: str) -> tuple[list[Document], int]:
        """List documents for a project."""
        await self.project_service.get_project(project_id, user_id)
        return await self.repo.list_by_project(project_id)
