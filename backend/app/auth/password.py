"""
AI Boardroom — Password Utilities
Password reset token generation and validation.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError as JWTInvalidTokenError

from app.core.config import get_settings


def create_password_reset_token(email: str) -> str:
    """Generate a short-lived token for password reset (15 mins)."""
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode = {"sub": email, "exp": expire, "type": "password_reset"}
    
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    """Verify reset token and extract the email address."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("type") != "password_reset":
            return None
        return payload.get("sub")
    except (JWTInvalidTokenError, Exception):
        return None
