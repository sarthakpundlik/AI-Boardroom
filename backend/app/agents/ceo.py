"""
AI Boardroom — CEO Agent
The Chief Executive Officer agent that orchestrates and synthesizes.
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

from app.ai.llm import get_reasoning_llm
from app.ai.structured_outputs import CEOFinalReportOutput
from app.memory.agent_memory import AgentMemory


class CEOAgent:
    """Chief Executive Officer. Orchestrates the session and makes final decisions."""

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self.role_name = "CEO"
        self.persona_desc = "Chief Executive Officer. Focuses on overall vision, strategic alignment, resolving conflicts among the C-suite, and making final actionable decisions."
        self.llm = get_reasoning_llm()
        self.memory = AgentMemory(session_id, self.role_name)

    async def synthesize(
        self,
        project_description: str,
        session_context: str,
        discussion_timeline: str,
    ) -> CEOFinalReportOutput:
        """Synthesize all agent inputs into a final executive report."""
        
        system_instruction = f"""
        You are {self.role_name}: {self.persona_desc}

        You are concluding an executive boardroom session. Review the discussion timeline containing the insights of your specialized C-suite agents.
        Your job is to:
        1. Resolve any conflicting advice between agents.
        2. Synthesize a unified strategic plan.
        3. Make definitive decisions.

        Project Overview:
        {project_description}

        Session Context:
        {session_context}

        Discussion Timeline (Inputs from C-Suite):
        {discussion_timeline}
        
        Provide your final synthesis adhering strictly to the output schema.
        """

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_instruction),
            ("user", "Please provide the final executive synthesis.")
        ])

        structured_llm = self.llm.with_structured_output(CEOFinalReportOutput)
        
        # Invoke LLM
        messages = prompt.format_messages()
        response: CEOFinalReportOutput = await structured_llm.ainvoke(messages)
        
        # Save scratchpad
        await self.memory.set_scratchpad(response.executive_summary)
        
        return response
