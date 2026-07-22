"""
AI Boardroom — Project Service
Business logic for Project management.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InsufficientPermissionsError, NotFoundError
from app.projects.models import Project
from app.projects.repository import ProjectRepository
from app.projects.schemas import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service layer for projects."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = ProjectRepository(session)

    async def create_project(self, user_id: str, data: ProjectCreate) -> Project:
        """Create a new project."""
        project = Project(
            title=data.title,
            description=data.description,
            input_type=data.input_type,
            user_id=user_id,
        )
        return await self.repo.create(project)

    async def get_project(self, project_id: str, user_id: str) -> Project:
        """Get a project by ID, ensuring ownership."""
        project = await self.repo.get_by_id_and_user(project_id, user_id)
        if not project:
            # Check if it exists at all to return 403 vs 404
            exists = await self.repo.get_by_id(project_id)
            if exists:
                raise InsufficientPermissionsError("You do not own this project")
            raise NotFoundError("Project", project_id)
        return project

    async def list_projects(
        self, user_id: str, page: int = 1, per_page: int = 20
    ) -> tuple[list[Project], int]:
        """List user's projects with pagination."""
        return await self.repo.list_by_user(user_id, page=page, per_page=per_page)

    async def update_project(
        self, project_id: str, user_id: str, data: ProjectUpdate
    ) -> Project:
        """Update a project."""
        project = await self.get_project(project_id, user_id)

        if data.title is not None:
            project.title = data.title
        if data.description is not None:
            project.description = data.description
        if data.input_type is not None:
            project.input_type = data.input_type
        if data.status is not None:
            project.status = data.status

        return await self.repo.update(project)

    async def delete_project(self, project_id: str, user_id: str) -> None:
        """Delete a project."""
        project = await self.get_project(project_id, user_id)
        await self.repo.delete(project)
