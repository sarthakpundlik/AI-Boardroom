"""
AI Boardroom — PDF Generator
Generates PDF files from the JSON report output.
"""

from __future__ import annotations

from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from app.core.logging import get_logger

logger = get_logger(__name__)


def generate_pdf_from_report(title: str, content_dict: dict) -> bytes:
    """
    Generate a simple PDF from the CEO's structured output.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    # Executive Summary
    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Paragraph(content_dict.get("executive_summary", ""), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Strategic Plan
    story.append(Paragraph("Strategic Plan", styles["Heading2"]))
    story.append(Paragraph(content_dict.get("strategic_plan", ""), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Key Decisions
    story.append(Paragraph("Key Decisions", styles["Heading2"]))
    for decision in content_dict.get("key_decisions", []):
        story.append(Paragraph(f"• {decision}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Dissenting Opinions
    story.append(Paragraph("Resolution of Dissenting Opinions", styles["Heading2"]))
    story.append(Paragraph(content_dict.get("dissenting_opinions_resolved", ""), styles["Normal"]))

    try:
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    except Exception as e:
        logger.error("PDF generation failed", error=str(e))
        return b""
