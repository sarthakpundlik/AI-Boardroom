"""
AI Boardroom — Orchestrator Graph
LangGraph flow construction.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.orchestrator.nodes import advance_round, ceo_node, get_agent_node, route_agents
from app.orchestrator.state import BoardroomState


def build_boardroom_graph(selected_agents: list[str]) -> StateGraph:
    """Build the LangGraph workflow based on selected agents."""
    
    workflow = StateGraph(BoardroomState)
    
    # 1. Add all specialized agent nodes
    for agent_name in selected_agents:
        workflow.add_node(agent_name, get_agent_node(agent_name))
        
    # 2. Add control nodes
    workflow.add_node("advance_round", advance_round)
    workflow.add_node("ceo_node", ceo_node)
    
    # 3. Define edges
    # START -> specialized agents (parallel)
    for agent_name in selected_agents:
        workflow.add_edge(START, agent_name)
        # Agents -> advance_round
        workflow.add_edge(agent_name, "advance_round")
        
    # After advancing round, we check if we should loop or go to CEO
    workflow.add_conditional_edges(
        "advance_round",
        route_agents,
        {
            # If routing returns an agent name, go to it (we map list of agents dynamically)
            **{agent: agent for agent in selected_agents},
            "ceo_node": "ceo_node",
        }
    )
    
    # CEO -> END
    workflow.add_edge("ceo_node", END)
    
    return workflow.compile()
