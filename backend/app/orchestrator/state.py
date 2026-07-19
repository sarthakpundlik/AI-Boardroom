"""
AI Boardroom — Orchestrator State
LangGraph state definition.
"""

from __future__ import annotations

import operator
from typing import Annotated, Sequence, TypedDict



class BoardroomState(TypedDict):
    """The state of the boardroom discussion passed between agents."""
    
    # Project context
    session_id: str
    project_id: str
    project_description: str
    
    # Retrieved data
    rag_context: str
    
    # Memory
    timeline: Annotated[Sequence[str], operator.add]
    
    # Control flow
    current_round: int
    max_rounds: int
    selected_agents: list[str]
    
    # Outputs
    final_report: dict | None
