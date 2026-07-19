"""
AI Boardroom — Report Repository
Data access layer for Reports.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reports.models import Report


class ReportRepository:
    """Repository for Report data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, report: Report) -> Report:
        """Store a new report."""
        self.session.add(report)
        await self.session.flush()
        await self.session.refresh(report)
        return report

    async def get_by_id(self, report_id: str) -> Report | None:
        """Get a report by ID."""
        result = await self.session.execute(
            select(Report).where(Report.id == report_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: str) -> tuple[list[Report], int]:
        """List reports for a project."""
        query = select(Report).where(Report.project_id == project_id)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(Report.created_at.desc())
        result = await self.session.execute(query)
        reports = list(result.scalars().all())

        return reports, total
