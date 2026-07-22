"""
AI Boardroom — CCO Agent
Chief Compliance Officer persona.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class CCOAgent(BaseAgent):
    """Chief Compliance Officer."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            session_id=session_id,
            role_name="CCO",
            persona_desc="Chief Compliance Officer. Focuses on legal risks, regulatory compliance, corporate governance, and ethical standards."
        )
