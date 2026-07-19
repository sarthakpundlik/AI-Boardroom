"""
AI Boardroom — CDO Agent
Chief Data Officer persona.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class CDOAgent(BaseAgent):
    """Chief Data Officer."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            session_id=session_id,
            role_name="CDO",
            persona_desc="Chief Data Officer. Focuses on data strategy, analytics, data governance, AI/ML utilization, and extracting actionable metrics from internal/external data sources."
        )
