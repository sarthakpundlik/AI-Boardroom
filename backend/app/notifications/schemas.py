"""
AI Boardroom — Notification Schemas
Pydantic schemas for notifications.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    """Notification returned to client."""
    id: str
    user_id: str
    title: str
    message: str
    type: str
    reference_id: str | None = None
    is_read: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class NotificationListResponse(BaseModel):
    """List of notifications."""
    notifications: list[NotificationResponse]
    total: int
    unread_count: int
