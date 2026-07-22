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
    GITHUB = "github"
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
# Mirrors the actually-implemented agent classes in
# app/agents/ceo.py and app/agents/specialized/*.py, and the
# AGENT_MAP keys in app/orchestrator/nodes.py. Keep these three
# in lockstep — this enum is the single source of truth that the
# frontend (src/data/agents.js) also mirrors.
# ============================================================
class AgentName(str, Enum):
    CEO = "CEO"
    CFO = "CFO"
    CTO = "CTO"
    CMO = "CMO"
    COO = "COO"
    CISO = "CISO"
    CHRO = "CHRO"
    CCO = "CCO"
    CDO = "CDO"


# ============================================================
# Agent Colors (for UI integration)
# ============================================================
AGENT_COLORS: dict[str, str] = {
    AgentName.CEO: "#FFD700",   # Premium Gold
    AgentName.CFO: "#10B981",   # Emerald Green — finance
    AgentName.CTO: "#8B5CF6",   # Violet — technology
    AgentName.CMO: "#F59E0B",   # Amber — marketing
    AgentName.COO: "#00D4FF",   # Electric Cyan — operations
    AgentName.CISO: "#FF4D4D",  # Risk Red — security
    AgentName.CHRO: "#EC4899",  # Pink — people
    AgentName.CCO: "#2563EB",   # Electric Blue — compliance
    AgentName.CDO: "#06B6D4",   # Cyan — data
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
# Maps input types to the set of specialized agents that should
# be activated. The CEO always runs separately as the final
# synthesis step (see orchestrator/graph.py) and is never listed here.
# ============================================================
AGENT_SELECTION_MATRIX: dict[InputType, list[AgentName]] = {
    InputType.STARTUP_IDEA: [
        AgentName.CFO, AgentName.CMO, AgentName.COO, AgentName.CISO,
    ],
    InputType.DATASET_ANALYSIS: [
        AgentName.CDO, AgentName.CFO, AgentName.COO,
    ],
    InputType.RESEARCH_PAPER: [
        AgentName.CTO, AgentName.CDO, AgentName.CISO,
    ],
    InputType.PRODUCT_PROPOSAL: [
        AgentName.CTO, AgentName.CMO, AgentName.COO, AgentName.CISO,
    ],
    InputType.FINANCIAL_REPORT: [
        AgentName.CFO, AgentName.CCO, AgentName.COO,
    ],
    InputType.MARKETING_STRATEGY: [
        AgentName.CMO, AgentName.COO, AgentName.CFO,
    ],
    InputType.TECHNICAL_ARCHITECTURE: [
        AgentName.CTO, AgentName.CISO, AgentName.COO,
    ],
    InputType.INVESTMENT_DUE_DILIGENCE: [
        AgentName.CFO, AgentName.CCO, AgentName.COO, AgentName.CISO,
    ],
    InputType.ORGANIZATIONAL_DECISION: [
        AgentName.CHRO, AgentName.COO, AgentName.CCO,
    ],
    InputType.GENERAL: [
        AgentName.CFO, AgentName.CTO, AgentName.CMO, AgentName.COO,
        AgentName.CISO, AgentName.CHRO, AgentName.CCO, AgentName.CDO,
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
    AIProvider.GEMINI,
    AIProvider.OPENAI,
    AIProvider.ANTHROPIC,
]


# ============================================================
# RAG Configuration
# ============================================================
EMBEDDING_DIMENSION: int = 768  # Gemini text-embedding-004
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200
MAX_CONTEXT_TOKENS: int = 500_000
TOP_K_RETRIEVAL: int = 10
