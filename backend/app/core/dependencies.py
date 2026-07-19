"""
AI Boardroom — FastAPI Dependencies
Reusable dependency injections for routes: DB sessions, auth, rate limiting.
"""

from __future__ import annotations

from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings
from app.core.constants import UserRole
from app.core.exceptions import (
    AuthenticationError,
    InsufficientPermissionsError,
    InvalidTokenError,
)

# HTTP Bearer scheme for JWT
security_scheme = HTTPBearer(auto_error=False)


async def get_db() -> AsyncGenerator:
    """Provide an async database session, auto-committed on success."""
    from app.database.session import async_session_factory

    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    settings: Settings = Depends(get_settings),
):
    """
    Decode and validate JWT from Authorization header.
    Returns the user record from the database.
    """
    if credentials is None:
        raise AuthenticationError("Authorization header missing")

    from app.auth.jwt_handler import decode_access_token
    from app.database.session import async_session_factory
    from app.users.repository import UserRepository

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise InvalidTokenError()

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise InvalidTokenError()

    async with async_session_factory() as session:
        repo = UserRepository(session)
        user = await repo.get_by_id(user_id)
        if user is None:
            raise AuthenticationError("User not found")
        return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    """Ensure the current user account is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )
    return current_user


async def require_admin(current_user=Depends(get_current_active_user)):
    """Require the current user to have admin role."""
    if current_user.role != UserRole.ADMIN:
        raise InsufficientPermissionsError("Admin access required")
    return current_user


def get_settings_dep() -> Settings:
    """Dependency wrapper for settings."""
    return get_settings()
