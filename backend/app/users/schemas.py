"""
AI Boardroom — User Schemas
Pydantic schemas for user request/response validation.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Shared user fields."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a new user via email/password."""

    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    name: str | None = Field(None, min_length=1, max_length=255)
    avatar_url: str | None = None


class UserResponse(UserBase):
    """Public user response — returned from API."""

    id: str
    role: str
    is_active: bool
    oauth_provider: str
    avatar_url: str | None = None
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    """Paginated list of users."""

    users: list[UserResponse]
    total: int
    page: int
    per_page: int


class ChangePasswordRequest(BaseModel):
    """Schema for changing password."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
