"""
AI Boardroom — Upload Repository
Data access layer for Documents.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.uploads.models import Document


class DocumentRepository:
    """Repository for Document data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, document: Document) -> Document:
        """Store document metadata."""
        self.session.add(document)
        await self.session.flush()
        await self.session.refresh(document)
        return document

    async def get_by_id(self, document_id: str) -> Document | None:
        """Get a document by ID."""
        result = await self.session.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: str) -> tuple[list[Document], int]:
        """List all documents for a project."""
        query = select(Document).where(Document.project_id == project_id)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(Document.created_at.desc())
        result = await self.session.execute(query)
        documents = list(result.scalars().all())

        return documents, total

    async def update_status(self, document_id: str, status: str, error_message: str | None = None) -> Document | None:
        """Update the processing status of a document."""
        doc = await self.get_by_id(document_id)
        if doc:
            doc.status = status
            if error_message:
                doc.error_message = error_message
            await self.session.flush()
        return doc
