"""
AI Boardroom — Session Repository
Data access layer for Session entity.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.sessions.models import Session


class SessionRepository:
    """Repository for Session data access."""

    def __init__(self, db_session: AsyncSession) -> None:
        self.session = db_session

    async def create(self, session_obj: Session) -> Session:
        """Create a new session."""
        self.session.add(session_obj)
        await self.session.flush()
        await self.session.refresh(session_obj)
        return session_obj

    async def get_by_id(self, session_id: str) -> Session | None:
        """Get a session by ID with its project."""
        result = await self.session.execute(
            select(Session)
            .options(selectinload(Session.project))
            .where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(
        self, project_id: str, page: int = 1, per_page: int = 20
    ) -> tuple[list[Session], int]:
        """List sessions for a specific project."""
        query = select(Session).where(Session.project_id == project_id)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Get paginated results
        query = query.order_by(Session.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        sessions = list(result.scalars().all())

        return sessions, total

    async def update(self, session_obj: Session) -> Session:
        """Update an existing session."""
        await self.session.flush()
        await self.session.refresh(session_obj)
        return session_obj

    async def delete(self, session_obj: Session) -> None:
        """Delete a session."""
        await self.session.delete(session_obj)
        await self.session.flush()
