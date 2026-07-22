"""
AI Boardroom — Prompts
Base prompt templates for the agents.
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate


# Base instructions for ALL agents
BASE_SYSTEM_INSTRUCTIONS = """
You are {agent_role}, participating in an executive boardroom session.
Your goal is to provide deep, analytical, and actionable insights based on the provided context.

Project Overview:
{project_description}

Current Session Context:
{session_context}

Available Documents / Data:
{rag_context}

Shared Timeline of the Discussion so far:
{discussion_timeline}

Your specific task for this round:
{task_instruction}

Respond strictly adhering to your defined persona and output schema.
"""

def build_agent_prompt() -> ChatPromptTemplate:
    """Build the dynamic prompt template for agents."""
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(BASE_SYSTEM_INSTRUCTIONS)
    ])
