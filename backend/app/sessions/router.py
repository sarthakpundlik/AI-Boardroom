"""
AI Boardroom — Session Router
API endpoints for boardroom sessions.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.sessions.schemas import SessionCreate, SessionListResponse, SessionResponse
from app.sessions.service import SessionService
from app.users.models import User

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    data: SessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new boardroom session within a project."""
    service = SessionService(db)
    return await service.create_session(current_user.id, data)


@router.get("/project/{project_id}", response_model=SessionListResponse)
async def list_project_sessions(
    project_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List all sessions for a specific project."""
    service = SessionService(db)
    sessions, total = await service.list_sessions(project_id, current_user.id, page, per_page)
    return {
        "sessions": sessions,
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get details of a specific session."""
    service = SessionService(db)
    return await service.get_session(session_id, current_user.id)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a specific session."""
    service = SessionService(db)
    await service.delete_session(session_id, current_user.id)
