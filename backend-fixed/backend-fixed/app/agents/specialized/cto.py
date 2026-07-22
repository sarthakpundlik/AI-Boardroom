"""
AI Boardroom — CTO Agent
Chief Technology Officer persona.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class CTOAgent(BaseAgent):
    """Chief Technology Officer."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            session_id=session_id,
            role_name="CTO",
            persona_desc="Chief Technology Officer. Focuses on technical feasibility, architecture, scalability, security, tech stack selection, and engineering velocity. Pragmatic but forward-looking."
        )
