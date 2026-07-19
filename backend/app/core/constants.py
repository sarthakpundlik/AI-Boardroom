"""
AI Boardroom — Application Constants
Centralized constants used across the entire backend.
"""

from __future__ import annotations

from enum import Enum


# ============================================================
# User Roles
# ============================================================
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


# ============================================================
# OAuth Providers
# ============================================================
class OAuthProvider(str, Enum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    EMAIL = "email"


# ============================================================
# Project & Session Status
# ============================================================
class ProjectStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class SessionStatus(str, Enum):
    PENDING = "pending"
    PREPROCESSING = "preprocessing"
    AGENT_SELECTION = "agent_selection"
    ROUND_1 = "round_1"
    ROUND_2 = "round_2"
    ROUND_3 = "round_3"
    SYNTHESIS = "synthesis"
    REPORT_GENERATION = "report_generation"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================================
# Input Types — what users can submit
# ============================================================
class InputType(str, Enum):
    STARTUP_IDEA = "startup_idea"
    DATASET_ANALYSIS = "dataset_analysis"
    RESEARCH_PAPER = "research_paper"
    PRODUCT_PROPOSAL = "product_proposal"
    FINANCIAL_REPORT = "financial_report"
    MARKETING_STRATEGY = "marketing_strategy"
    TECHNICAL_ARCHITECTURE = "technical_architecture"
    INVESTMENT_DUE_DILIGENCE = "investment_due_diligence"
    ORGANIZATIONAL_DECISION = "organizational_decision"
    GENERAL = "general"


# ============================================================
# Agent Names
# ============================================================
class AgentName(str, Enum):
    CEO = "ceo"
    STRATEGIC = "strategic"
    BUSINESS = "business"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    CUSTOMER = "customer"
    RISK = "risk"
    DATA = "data"
    DEVIL = "devil"
    REVIEWER = "reviewer"


# ============================================================
# Agent Colors (for UI integration)
# ============================================================
AGENT_COLORS: dict[str, str] = {
    AgentName.CEO: "#FFD700",        # Premium Gold
    AgentName.STRATEGIC: "#2563EB",  # Electric Blue
    AgentName.BUSINESS: "#00D4FF",   # Electric Cyan
    AgentName.FINANCIAL: "#10B981",  # Emerald Green
    AgentName.TECHNICAL: "#8B5CF6",  # Violet
    AgentName.CUSTOMER: "#F59E0B",   # Amber
    AgentName.RISK: "#FF4D4D",       # Risk Red
    AgentName.DATA: "#06B6D4",       # Cyan
    AgentName.DEVIL: "#EF4444",      # Red
    AgentName.REVIEWER: "#FFD700",   # Gold
}


# ============================================================
# Discussion Rounds
# ============================================================
class DiscussionRound(int, Enum):
    INDEPENDENT = 1
    PEER_REVIEW = 2
    CHALLENGE = 3


MAX_DISCUSSION_ROUNDS = 3


# ============================================================
# Decision Outcomes
# ============================================================
class DecisionOutcome(str, Enum):
    GO = "go"
    GO_WITH_MODIFICATIONS = "go_with_modifications"
    NEEDS_FURTHER_RESEARCH = "needs_further_research"
    NOT_RECOMMENDED = "not_recommended"


# ============================================================
# Report Types
# ============================================================
class ReportType(str, Enum):
    STRATEGIC = "strategic_report"
    BUSINESS = "business_report"
    FINANCIAL = "financial_report"
    TECHNICAL = "technical_report"
    CUSTOMER = "customer_report"
    RISK = "risk_report"
    DATA = "data_report"
    CONTRARIAN = "contrarian_report"
    BOARDROOM_DISCUSSION = "boardroom_discussion"
    EXECUTIVE_SUMMARY = "executive_summary"


class ExportFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPT = "ppt"


# ============================================================
# File Types
# ============================================================
ALLOWED_FILE_EXTENSIONS: set[str] = {
    ".pdf", ".docx", ".pptx", ".csv", ".xlsx", ".json", ".txt"
}

ALLOWED_MIME_TYPES: set[str] = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/json",
    "text/plain",
}

MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024    # 50 MB
MAX_SESSION_SIZE_BYTES: int = 200 * 1024 * 1024  # 200 MB


# ============================================================
# Dynamic Agent Selection Matrix
# Maps input types to the set of agents that should be activated.
# CEO and Reviewer are ALWAYS activated.
# ============================================================
AGENT_SELECTION_MATRIX: dict[InputType, list[AgentName]] = {
    InputType.STARTUP_IDEA: [
        AgentName.STRATEGIC, AgentName.BUSINESS, AgentName.FINANCIAL,
        AgentName.CUSTOMER, AgentName.RISK, AgentName.DEVIL,
    ],
    InputType.DATASET_ANALYSIS: [
        AgentName.DATA, AgentName.FINANCIAL, AgentName.BUSINESS, AgentName.RISK,
    ],
    InputType.RESEARCH_PAPER: [
        AgentName.TECHNICAL, AgentName.STRATEGIC, AgentName.RISK, AgentName.DEVIL,
    ],
    InputType.PRODUCT_PROPOSAL: [
        AgentName.BUSINESS, AgentName.TECHNICAL, AgentName.CUSTOMER,
        AgentName.RISK, AgentName.STRATEGIC,
    ],
    InputType.FINANCIAL_REPORT: [
        AgentName.FINANCIAL, AgentName.RISK, AgentName.BUSINESS, AgentName.STRATEGIC,
    ],
    InputType.MARKETING_STRATEGY: [
        AgentName.BUSINESS, AgentName.CUSTOMER, AgentName.STRATEGIC,
        AgentName.RISK, AgentName.DEVIL,
    ],
    InputType.TECHNICAL_ARCHITECTURE: [
        AgentName.TECHNICAL, AgentName.RISK, AgentName.STRATEGIC, AgentName.DEVIL,
    ],
    InputType.INVESTMENT_DUE_DILIGENCE: [
        AgentName.FINANCIAL, AgentName.BUSINESS, AgentName.STRATEGIC,
        AgentName.RISK, AgentName.CUSTOMER,
    ],
    InputType.ORGANIZATIONAL_DECISION: [
        AgentName.STRATEGIC, AgentName.RISK, AgentName.BUSINESS,
        AgentName.CUSTOMER, AgentName.DEVIL,
    ],
    InputType.GENERAL: [
        AgentName.STRATEGIC, AgentName.BUSINESS, AgentName.FINANCIAL,
        AgentName.TECHNICAL, AgentName.CUSTOMER, AgentName.RISK,
        AgentName.DATA, AgentName.DEVIL,
    ],
}


# ============================================================
# AI Model Configuration
# ============================================================
class AIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


AI_MODEL_PRIORITY: list[AIProvider] = [
    AIProvider.OPENAI,
    AIProvider.ANTHROPIC,
    AIProvider.GEMINI,
]


# ============================================================
# RAG Configuration
# ============================================================
EMBEDDING_DIMENSION: int = 1536  # OpenAI text-embedding-3-small
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200
MAX_CONTEXT_TOKENS: int = 500_000
TOP_K_RETRIEVAL: int = 10
