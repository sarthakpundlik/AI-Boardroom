"""
AI Boardroom — Auth Schemas
Pydantic schemas for login, tokens, and registration.
"""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    """Response containing access and refresh tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds


class LoginRequest(BaseModel):
    """Email/password login request."""

    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Request to refresh access token."""

    refresh_token: str


class OAuthCallbackRequest(BaseModel):
    """Callback data from OAuth providers."""

    code: str
    state: str | None = None


class PasswordResetRequest(BaseModel):
    """Request to send password reset email."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with token."""

    token: str
    new_password: str = Field(..., min_length=8, max_length=128)
