"""
AI Boardroom — Uploads Router
API endpoints for uploading files to projects.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.uploads.schemas import DocumentListResponse, DocumentResponse
from app.uploads.service import UploadService
from app.users.models import User

router = APIRouter(prefix="/uploads", tags=["Uploads"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload a file to a project."""
    service = UploadService(db)
    return await service.upload_document(project_id, current_user.id, file)


@router.get("/project/{project_id}", response_model=DocumentListResponse)
async def list_project_documents(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List all documents uploaded to a specific project."""
    service = UploadService(db)
    documents, total = await service.list_documents(project_id, current_user.id)
    return {
        "documents": documents,
        "total": total,
    }
