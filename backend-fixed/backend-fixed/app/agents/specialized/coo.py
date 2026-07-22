"""
AI Boardroom — COO Agent
Chief Operating Officer persona.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class COOAgent(BaseAgent):
    """Chief Operating Officer."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            session_id=session_id,
            role_name="COO",
            persona_desc="Chief Operating Officer. Focuses on execution, supply chain, internal processes, resource allocation, and scaling operations efficiently. Highly practical and logistics-oriented."
        )
