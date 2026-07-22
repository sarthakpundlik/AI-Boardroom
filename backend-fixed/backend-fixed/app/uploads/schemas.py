"""
AI Boardroom — Upload Schemas
Pydantic schemas for upload API.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """Properties of an uploaded document."""
    id: str
    project_id: str
    user_id: str
    filename: str
    mime_type: str
    file_size_bytes: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):
    """List of documents for a project."""
    documents: list[DocumentResponse]
    total: int
