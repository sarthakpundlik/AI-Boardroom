"""
AI Boardroom — Orchestrator Nodes
Graph nodes representing agent actions.
"""

from __future__ import annotations

from app.agents.ceo import CEOAgent
from app.agents.specialized import (
    CCOAgent,
    CDOAgent,
    CFOAgent,
    CHROAgent,
    CISOAgent,
    CMOAgent,
    COOAgent,
    CTOAgent,
)
from app.core.logging import get_logger
from app.memory.session_memory import SessionMemory
from app.orchestrator.state import BoardroomState

logger = get_logger(__name__)

# Map strings to classes
AGENT_MAP = {
    "CFO": CFOAgent,
    "CTO": CTOAgent,
    "CMO": CMOAgent,
    "COO": COOAgent,
    "CISO": CISOAgent,
    "CHRO": CHROAgent,
    "CCO": CCOAgent,
    "CDO": CDOAgent,
}


async def route_agents(state: BoardroomState):
    """Determine which agents to call next."""
    if state["current_round"] > state["max_rounds"]:
        return "ceo_node"
    # Otherwise we map to all selected agents in parallel (LangGraph supports parallel execution)
    return state["selected_agents"]


def get_agent_node(agent_name: str):
    """Factory for agent nodes."""
    
    async def agent_node(state: BoardroomState) -> dict:
        logger.info(f"Running {agent_name} node", round=state["current_round"])
        
        agent_cls = AGENT_MAP.get(agent_name)
        if not agent_cls:
            return {"timeline": [f"[{agent_name}] Agent not configured."]}
            
        agent = agent_cls(state["session_id"])
        
        # Format timeline from state
        timeline_str = "\n".join(state["timeline"]) if state["timeline"] else "No discussion yet."
        
        # Analyze
        output = await agent.analyze(
            project_description=state["project_description"],
            session_context=f"Round {state['current_round']} of {state['max_rounds']}",
            rag_context=state["rag_context"],
            discussion_timeline=timeline_str,
            task_instruction="Review the data and provide your specific departmental analysis.",
        )
        
        # Update session memory
        session_memory = SessionMemory(state["session_id"])
        await session_memory.add_message(agent_name, output.summary)
        
        # Return state update (append to timeline)
        return {
            "timeline": [f"[{agent_name} Round {state['current_round']}]: {output.summary}"]
        }

    return agent_node


async def ceo_node(state: BoardroomState) -> dict:
    """The CEO synthesizes the final report."""
    logger.info("Running CEO node (Final Synthesis)")
    
    ceo = CEOAgent(state["session_id"])
    timeline_str = "\n".join(state["timeline"])
    
    report = await ceo.synthesize(
        project_description=state["project_description"],
        session_context="Final Synthesis",
        discussion_timeline=timeline_str,
    )
    
    return {
        "final_report": report.model_dump()
    }


async def advance_round(state: BoardroomState) -> dict:
    """Increment the round counter."""
    return {"current_round": state["current_round"] + 1}
