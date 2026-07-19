"""
AI Boardroom — Notification Router
API endpoints for checking and marking notifications.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.notifications.schemas import NotificationListResponse, NotificationResponse
from app.notifications.service import NotificationService
from app.users.models import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's notifications."""
    service = NotificationService(db)
    notifications, total, unread = await service.list_notifications(current_user.id, page, per_page)
    return {
        "notifications": notifications,
        "total": total,
        "unread_count": unread,
    }


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a specific notification as read."""
    service = NotificationService(db)
    return await service.mark_as_read(notification_id, current_user.id)


@router.post("/read-all", response_model=dict)
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark all unread notifications as read."""
    service = NotificationService(db)
    count = await service.mark_all_as_read(current_user.id)
    return {"message": f"{count} notifications marked as read."}
