"""
AI Boardroom — Structured Outputs
Pydantic schemas used for coercing LLM outputs.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.core.constants import DecisionOutcome


class AgentAnalysisOutput(BaseModel):
    """Standard output schema for an agent's analysis round."""
    summary: str = Field(description="A concise 1-2 sentence summary of your analysis.")
    detailed_findings: list[str] = Field(description="List of specific, deep analytical points derived from the context.")
    risks_identified: list[str] = Field(description="Any risks, anomalies, or concerns found.")
    recommendations: list[str] = Field(description="Actionable next steps based on your domain expertise.")
    confidence_score: int = Field(description="Your confidence in this analysis from 1-100.")


class CEOFinalReportOutput(BaseModel):
    """Output schema for the CEO agent's final synthesis."""
    executive_summary: str = Field(description="Overall summary of the entire boardroom session.")
    key_decisions: list[str] = Field(description="Decisions made based on the agents' input.")
    strategic_plan: str = Field(description="A detailed strategic plan for the next steps.")
    dissenting_opinions_resolved: str = Field(description="How conflicting agent viewpoints were resolved.")
    decision_outcome: DecisionOutcome = Field(
        description="The board's overall verdict on the proposal: go, go_with_modifications, "
        "needs_further_research, or not_recommended."
    )
