"""
AI Boardroom — Auth Repository
Data access for refresh tokens.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import RefreshToken


class AuthRepository:
    """Repository for authentication related data (e.g., refresh tokens)."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_refresh_token(
        self, user_id: str, token: str, expires_at: datetime, device_info: str | None = None
    ) -> RefreshToken:
        """Store a new refresh token."""
        db_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            device_info=device_info,
        )
        self.session.add(db_token)
        await self.session.flush()
        return db_token

    async def get_refresh_token(self, token: str) -> RefreshToken | None:
        """Get a refresh token record."""
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, token: str) -> bool:
        """Mark a refresh token as revoked."""
        db_token = await self.get_refresh_token(token)
        if db_token:
            db_token.is_revoked = True
            await self.session.flush()
            return True
        return False

    async def revoke_all_user_tokens(self, user_id: str) -> None:
        """Revoke all active refresh tokens for a user (e.g., on password change)."""
        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False  # noqa: E712
            )
        )
        for token in result.scalars():
            token.is_revoked = True
        await self.session.flush()

    async def delete_expired_tokens(self, before_time: datetime) -> int:
        """Cleanup task to delete old tokens."""
        result = await self.session.execute(
            delete(RefreshToken).where(RefreshToken.expires_at < before_time)
        )
        await self.session.flush()
        return result.rowcount
