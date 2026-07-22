"""
AI Boardroom — JWT Handler
Token generation, decoding, and validation logic.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError as JWTInvalidTokenError

from app.core.config import get_settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a new JWT access token."""
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": int(expire.timestamp()), "type": "access"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create a new JWT refresh token."""
    settings = get_settings()
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({"exp": int(expire.timestamp()), "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str, expected_type: str | None = None) -> dict | None:
    """Decode and validate a JWT token."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if expected_type and payload.get("type") != expected_type:
            return None
        return payload
    except (JWTInvalidTokenError, ExpiredSignatureError):
        return None


def decode_access_token(token: str) -> dict | None:
    """Decode an access token specifically."""
    return decode_token(token, expected_type="access")


def decode_refresh_token(token: str) -> dict | None:
    """Decode a refresh token specifically."""
    return decode_token(token, expected_type="refresh")