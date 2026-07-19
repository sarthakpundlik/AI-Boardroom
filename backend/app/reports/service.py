"""
AI Boardroom — Report Service
Business logic for generating and retrieving reports.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.projects.service import ProjectService
from app.reports.generator import generate_pdf_from_report
from app.reports.models import Report
from app.reports.repository import ReportRepository
from app.storage.manager import StorageManager


class ReportService:
    """Service layer for handling boardroom reports."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ReportRepository(session)
        self.project_service = ProjectService(session)
        self.storage_manager = StorageManager()

    async def create_report(
        self, session_id: str, project_id: str, user_id: str, ceo_output: dict
    ) -> Report:
        """Create a new report from the CEO's synthesis and generate a PDF."""
        # Ensure project exists
        project = await self.project_service.get_project(project_id, user_id)
        
        title = f"{project.title} - Final Boardroom Report"
        
        # Generate PDF
        pdf_bytes = generate_pdf_from_report(title, ceo_output)
        
        pdf_url = None
        if pdf_bytes:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"reports/{project_id}/{timestamp}_{unique_id}_report.pdf"
            
            # Save to storage (S3 or Local)
            pdf_url = await self.storage_manager.save_file(pdf_bytes, filename)

        report = Report(
            session_id=session_id,
            project_id=project_id,
            user_id=user_id,
            title=title,
            summary=ceo_output.get("executive_summary", "No summary available"),
            full_content=ceo_output,
            pdf_url=pdf_url,
        )
        return await self.repo.create(report)

    async def get_report(self, report_id: str, user_id: str) -> Report:
        """Get a report, ensuring ownership through the project."""
        report = await self.repo.get_by_id(report_id)
        if not report:
            raise NotFoundError("Report", report_id)
            
        # Verify ownership
        await self.project_service.get_project(report.project_id, user_id)
        
        return report

    async def list_project_reports(self, project_id: str, user_id: str) -> tuple[list[Report], int]:
        """List all reports for a given project."""
        await self.project_service.get_project(project_id, user_id)
        return await self.repo.list_by_project(project_id)
