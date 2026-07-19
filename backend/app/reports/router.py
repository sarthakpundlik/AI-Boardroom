"""
AI Boardroom — Report Router
API endpoints for accessing generated reports.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.reports.schemas import ReportListResponse, ReportResponse
from app.reports.service import ReportService
from app.users.models import User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/project/{project_id}", response_model=ReportListResponse)
async def list_project_reports(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List all reports for a specific project."""
    service = ReportService(db)
    reports, total = await service.list_project_reports(project_id, current_user.id)
    return {
        "reports": reports,
        "total": total,
    }


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get details of a specific report, including its full content and PDF URL."""
    service = ReportService(db)
    return await service.get_report(report_id, current_user.id)
