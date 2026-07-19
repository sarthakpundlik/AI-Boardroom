"""
AI Boardroom — CFO Agent
Chief Financial Officer persona.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class CFOAgent(BaseAgent):
    """Chief Financial Officer."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            session_id=session_id,
            role_name="CFO",
            persona_desc="Chief Financial Officer. Focuses on ROI, budget constraints, financial risks, revenue modeling, and cost-benefit analysis. Highly analytical and risk-averse regarding spending."
        )
