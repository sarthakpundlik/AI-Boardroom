"""
AI Boardroom — Project Repository
Data access layer for Project entity.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.projects.models import Project


class ProjectRepository:
    """Repository for Project data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, project: Project) -> Project:
        """Create a new project."""
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def get_by_id(self, project_id: str) -> Project | None:
        """Get a project by ID."""
        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_and_user(self, project_id: str, user_id: str) -> Project | None:
        """Get a project by ID ensuring it belongs to the user."""
        result = await self.session.execute(
            select(Project).where(
                Project.id == project_id,
                Project.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self, user_id: str, page: int = 1, per_page: int = 20
    ) -> tuple[list[Project], int]:
        """List projects for a specific user with pagination."""
        query = select(Project).where(Project.user_id == user_id)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Get paginated results
        query = query.order_by(Project.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        projects = list(result.scalars().all())

        return projects, total

    async def update(self, project: Project) -> Project:
        """Update an existing project."""
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def delete(self, project: Project) -> None:
        """Delete a project."""
        await self.session.delete(project)
        await self.session.flush()
