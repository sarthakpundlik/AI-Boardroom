"""
AI Boardroom — User Router
API endpoints for user profile management.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db, require_admin
from app.users.models import User
from app.users.schemas import ChangePasswordRequest, UserListResponse, UserResponse, UserUpdate
from app.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_active_user)):
    """Get the currently authenticated user's profile."""
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's profile."""
    service = UserService(db)
    return await service.update_profile(current_user.id, data)


@router.post("/me/change-password", response_model=UserResponse)
async def change_my_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Change current user's password."""
    service = UserService(db)
    return await service.change_password(current_user.id, data)


# --- Admin Routes ---

@router.get("", response_model=UserListResponse, dependencies=[Depends(require_admin)])
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List all users (Admin only)."""
    service = UserService(db)
    users, total = await service.list_users(page=page, per_page=per_page, search=search)
    return {
        "users": users,
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.delete("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
async def deactivate_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Deactivate a user account (Admin only)."""
    service = UserService(db)
    return await service.deactivate_user(user_id)
