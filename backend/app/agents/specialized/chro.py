"""
AI Boardroom — CHRO Agent
Chief Human Resources Officer persona.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class CHROAgent(BaseAgent):
    """Chief Human Resources Officer."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            session_id=session_id,
            role_name="CHRO",
            persona_desc="Chief Human Resources Officer. Focuses on talent acquisition, employee retention, company culture, organizational design, and labor relations."
        )
