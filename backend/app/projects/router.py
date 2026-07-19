"""
AI Boardroom — Project Router
API endpoints for project management.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.projects.schemas import ProjectCreate, ProjectListResponse, ProjectResponse, ProjectUpdate
from app.projects.service import ProjectService
from app.users.models import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new project."""
    service = ProjectService(db)
    return await service.create_project(current_user.id, data)


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List projects belonging to the current user."""
    service = ProjectService(db)
    projects, total = await service.list_projects(current_user.id, page, per_page)
    return {
        "projects": projects,
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific project."""
    service = ProjectService(db)
    return await service.get_project(project_id, current_user.id)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a specific project."""
    service = ProjectService(db)
    return await service.update_project(project_id, current_user.id, data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a specific project."""
    service = ProjectService(db)
    await service.delete_project(project_id, current_user.id)
