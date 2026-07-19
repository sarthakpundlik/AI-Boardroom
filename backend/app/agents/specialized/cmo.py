"""
AI Boardroom — CMO Agent
Chief Marketing Officer persona.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class CMOAgent(BaseAgent):
    """Chief Marketing Officer."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            session_id=session_id,
            role_name="CMO",
            persona_desc="Chief Marketing Officer. Focuses on go-to-market strategy, brand positioning, customer acquisition, market trends, and competitive analysis. Highly attuned to user sentiment and market share."
        )
