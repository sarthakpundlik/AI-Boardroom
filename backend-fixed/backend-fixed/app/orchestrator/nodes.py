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
from app.websocket.events import EventType, format_event
from app.websocket.manager import manager

logger = get_logger(__name__)

# Map strings to classes — keys MUST match app.core.constants.AgentName values.
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
        session_id = state["session_id"]
        current_round = state["current_round"]
        logger.info(f"Running {agent_name} node", round=current_round)

        agent_cls = AGENT_MAP.get(agent_name)
        if not agent_cls:
            return {"timeline": [f"[{agent_name}] Agent not configured."]}

        await manager.broadcast_to_session(
            session_id,
            format_event(EventType.AGENT_STARTED, {"agent": agent_name, "round": current_round}),
        )

        agent = agent_cls(session_id)

        # Format timeline from state
        timeline_str = "\n".join(state["timeline"]) if state["timeline"] else "No discussion yet."

        try:
            output = await agent.analyze(
                project_description=state["project_description"],
                session_context=f"Round {current_round} of {state['max_rounds']}",
                rag_context=state["rag_context"],
                discussion_timeline=timeline_str,
                task_instruction="Review the data and provide your specific departmental analysis.",
            )
        except Exception as e:
            logger.error(f"{agent_name} analysis failed", error=str(e))
            await manager.broadcast_to_session(
                session_id,
                format_event(EventType.ERROR, {"agent": agent_name, "message": f"{agent_name} failed to respond."}),
            )
            return {
                "timeline": [f"[{agent_name} Round {current_round}]: (failed to respond)"],
            }

        # Best-effort session memory update — never let a Redis hiccup break the run.
        try:
            session_memory = SessionMemory(session_id)
            await session_memory.add_message(agent_name, output.summary)
        except Exception as e:
            logger.warning("Session memory unavailable, continuing without it", error=str(e))

        await manager.broadcast_to_session(
            session_id,
            format_event(
                EventType.AGENT_FINISHED,
                {"agent": agent_name, "round": current_round, "summary": output.summary},
            ),
        )

        finding = {
            "agent": agent_name,
            "round": current_round,
            "summary": output.summary,
            "detailed_findings": output.detailed_findings,
            "risks_identified": output.risks_identified,
            "recommendations": output.recommendations,
            "confidence_score": output.confidence_score,
        }

        return {
            "timeline": [f"[{agent_name} Round {current_round}]: {output.summary}"],
            "agent_findings": [finding],
        }

    return agent_node


async def ceo_node(state: BoardroomState) -> dict:
    """The CEO synthesizes the final report."""
    session_id = state["session_id"]
    logger.info("Running CEO node (Final Synthesis)")

    await manager.broadcast_to_session(session_id, format_event(EventType.CEO_STARTED, {}))

    ceo = CEOAgent(session_id)
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
    """Increment the round counter and notify listeners."""
    next_round = state["current_round"] + 1
    if next_round <= state["max_rounds"]:
        await manager.broadcast_to_session(
            state["session_id"],
            format_event(EventType.ROUND_ADVANCED, {"round": next_round}),
        )
    return {"current_round": next_round}
