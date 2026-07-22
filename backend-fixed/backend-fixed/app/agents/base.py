"""
AI Boardroom — Base Agent
Base class for all specialized agents.
"""

from __future__ import annotations


from langchain_google_genai import ChatGoogleGenerativeAI

from app.ai.llm import get_llm
from app.ai.prompts import BASE_SYSTEM_INSTRUCTIONS
from app.ai.structured_outputs import AgentAnalysisOutput
from app.memory.agent_memory import AgentMemory


class BaseAgent:
    """Base class for all boardroom agents."""

    def __init__(self, session_id: str, role_name: str, persona_desc: str) -> None:
        self.session_id = session_id
        self.role_name = role_name
        self.persona_desc = persona_desc
        self.llm: ChatGoogleGenerativeAI = get_llm(temperature=0.2)
        self.memory = AgentMemory(session_id, role_name)

    async def analyze(
        self,
        project_description: str,
        session_context: str,
        rag_context: str,
        discussion_timeline: str,
        task_instruction: str,
    ) -> AgentAnalysisOutput:
        """Perform analysis for the current round."""
        
        # Build System Prompt
        system_prompt = BASE_SYSTEM_INSTRUCTIONS.format(
            agent_role=f"{self.role_name}: {self.persona_desc}",
            project_description=project_description,
            session_context=session_context,
            rag_context=rag_context,
            discussion_timeline=discussion_timeline,
            task_instruction=task_instruction,
        )

        # We use the LLM with structured output coercion
        structured_llm = self.llm.with_structured_output(AgentAnalysisOutput)
        
        # Invoke LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Please provide your analysis for this round."},
        ]
        
        response: AgentAnalysisOutput = await structured_llm.ainvoke(messages)
        
        # Save scratchpad notes (just a summary of what they thought)
        await self.memory.set_scratchpad(response.summary)
        
        return response
