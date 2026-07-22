"""
AI Boardroom — Project Schemas
Pydantic schemas for project API requests and responses.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import InputType, ProjectStatus


class ProjectBase(BaseModel):
    """Shared properties."""
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    input_type: InputType = InputType.GENERAL


class ProjectCreate(ProjectBase):
    """Properties to receive on project creation."""
    pass


class ProjectUpdate(BaseModel):
    """Properties to receive on project update."""
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    input_type: InputType | None = None
    status: ProjectStatus | None = None


class ProjectResponse(ProjectBase):
    """Properties to return to client."""
    id: str
    user_id: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    """Paginated list of projects."""
    projects: list[ProjectResponse]
    total: int
    page: int
    per_page: int
