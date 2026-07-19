"""
AI Boardroom — User Repository
Data access layer for user operations.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


class UserRepository:
    """Repository pattern for User data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: str) -> User | None:
        """Get a user by their UUID."""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Get a user by email address."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_oauth(self, provider: str, oauth_id: str) -> User | None:
        """Get a user by OAuth provider and ID."""
        result = await self.session.execute(
            select(User).where(
                User.oauth_provider == provider,
                User.oauth_id == oauth_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Create a new user."""
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update(self, user: User) -> User:
        """Update an existing user."""
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update_last_login(self, user: User) -> None:
        """Update the user's last login timestamp."""
        user.last_login = datetime.now(timezone.utc)
        await self.session.flush()

    async def list_users(
        self,
        page: int = 1,
        per_page: int = 20,
        search: str | None = None,
    ) -> tuple[list[User], int]:
        """List users with pagination and optional search."""
        query = select(User)

        if search:
            query = query.where(
                User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%")
            )

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Get paginated results
        query = query.offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        users = list(result.scalars().all())

        return users, total

    async def deactivate(self, user: User) -> User:
        """Deactivate a user account."""
        user.is_active = False
        await self.session.flush()
        return user

    async def delete(self, user: User) -> None:
        """Hard delete a user (use deactivate instead in production)."""
        await self.session.delete(user)
        await self.session.flush()
