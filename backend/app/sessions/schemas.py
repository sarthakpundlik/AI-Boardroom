"""
AI Boardroom — Session Schemas
Pydantic schemas for session API requests and responses.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.core.constants import AgentName, SessionStatus


class SessionCreate(BaseModel):
    """Request to create a new boardroom session."""
    project_id: str


class SessionResponse(BaseModel):
    """Properties to return to client."""
    id: str
    project_id: str
    status: SessionStatus
    round_count: int
    agents_selected: list[AgentName]
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionListResponse(BaseModel):
    """Paginated list of sessions."""
    sessions: list[SessionResponse]
    total: int
    page: int
    per_page: int
