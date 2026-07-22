"""
AI Boardroom — User Service
Business logic layer for user management.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ValidationError
from app.core.logging import get_logger
from app.core.security import hash_password, verify_password, validate_password_strength
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import ChangePasswordRequest, UserUpdate

logger = get_logger(__name__)


class UserService:
    """Service layer for user operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)

    async def get_user(self, user_id: str) -> User:
        """Get a user by ID or raise NotFoundError."""
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email (returns None if not found)."""
        return await self.repo.get_by_email(email)

    async def update_profile(self, user_id: str, data: UserUpdate) -> User:
        """Update user profile fields."""
        user = await self.get_user(user_id)

        if data.name is not None:
            user.name = data.name
        if data.avatar_url is not None:
            user.avatar_url = data.avatar_url

        return await self.repo.update(user)

    async def change_password(self, user_id: str, data: ChangePasswordRequest) -> User:
        """Change user password with validation."""
        user = await self.get_user(user_id)

        # Verify current password
        if not user.hashed_password or not verify_password(
            data.current_password, user.hashed_password
        ):
            raise ValidationError("Current password is incorrect")

        # Validate new password strength
        errors = validate_password_strength(data.new_password)
        if errors:
            raise ValidationError("Password does not meet requirements", detail=errors)

        # Check password history (last 5 passwords)
        if user.password_history:
            past_hashes = user.password_history.split("|")
            for past_hash in past_hashes[-5:]:
                if verify_password(data.new_password, past_hash):
                    raise ValidationError("Cannot reuse any of the last 5 passwords")

        # Update password and history
        new_hash = hash_password(data.new_password)
        old_history = user.password_history or ""
        user.password_history = (
            f"{old_history}|{user.hashed_password}" if old_history else user.hashed_password
        )
        user.hashed_password = new_hash

        logger.info("Password changed", user_id=user_id)
        return await self.repo.update(user)

    async def list_users(
        self, page: int = 1, per_page: int = 20, search: str | None = None
    ) -> tuple[list[User], int]:
        """List users with pagination."""
        return await self.repo.list_users(page=page, per_page=per_page, search=search)

    async def deactivate_user(self, user_id: str) -> User:
        """Deactivate a user account."""
        user = await self.get_user(user_id)
        logger.info("User deactivated", user_id=user_id)
        return await self.repo.deactivate(user)
