"""
AI Boardroom — Report Schemas
Pydantic schemas for retrieving reports.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ReportResponse(BaseModel):
    """Report response object."""
    id: str
    session_id: str
    project_id: str
    title: str
    summary: str
    full_content: dict
    pdf_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReportListResponse(BaseModel):
    """List of reports."""
    reports: list[ReportResponse]
    total: int
