"""
AI Boardroom — Session Service
Business logic for managing boardroom sessions.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InsufficientPermissionsError, NotFoundError
from app.projects.service import ProjectService
from app.sessions.models import Session
from app.sessions.repository import SessionRepository
from app.sessions.schemas import SessionCreate


class SessionService:
    """Service layer for boardroom sessions."""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
        self.repo = SessionRepository(db_session)
        self.project_service = ProjectService(db_session)

    async def create_session(self, user_id: str, data: SessionCreate) -> Session:
        """Create a new session within a project."""
        # Ensure project exists and belongs to user
        project = await self.project_service.get_project(data.project_id, user_id)

        # CEO logic to select agents based on project input_type will happen in Orchestrator
        # For now, we initialize an empty session
        session_obj = Session(project_id=project.id)
        return await self.repo.create(session_obj)

    async def get_session(self, session_id: str, user_id: str) -> Session:
        """Get a session, ensuring the user owns the parent project."""
        session_obj = await self.repo.get_by_id(session_id)
        if not session_obj:
            raise NotFoundError("Session", session_id)

        if session_obj.project.user_id != user_id:
            raise InsufficientPermissionsError("You do not own this session")

        return session_obj

    async def list_sessions(
        self, project_id: str, user_id: str, page: int = 1, per_page: int = 20
    ) -> tuple[list[Session], int]:
        """List sessions for a project, ensuring ownership."""
        # Verify ownership
        await self.project_service.get_project(project_id, user_id)
        return await self.repo.list_by_project(project_id, page=page, per_page=per_page)

    async def delete_session(self, session_id: str, user_id: str) -> None:
        """Delete a session."""
        session_obj = await self.get_session(session_id, user_id)
        await self.repo.delete(session_obj)
