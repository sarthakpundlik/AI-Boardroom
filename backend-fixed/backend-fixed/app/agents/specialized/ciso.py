"""
AI Boardroom — CISO Agent
Chief Information Security Officer persona.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class CISOAgent(BaseAgent):
    """Chief Information Security Officer."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            session_id=session_id,
            role_name="CISO",
            persona_desc="Chief Information Security Officer. Focuses on data privacy, cyber threats, compliance with regulations (GDPR/CCPA), vulnerability management, and risk mitigation."
        )
