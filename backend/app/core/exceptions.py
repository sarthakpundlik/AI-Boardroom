"""
AI Boardroom — Custom Exception Hierarchy
Structured exceptions with HTTP status codes for the API layer.
"""

from __future__ import annotations

from typing import Any


class AIBoardroomException(Exception):
    """Base exception for all AI Boardroom errors."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = 500,
        detail: Any = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


# ============================================================
# Authentication & Authorization
# ============================================================
class AuthenticationError(AIBoardroomException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message=message, status_code=401)


class InvalidCredentialsError(AuthenticationError):
    """Raised for invalid email/password."""

    def __init__(self) -> None:
        super().__init__(message="Invalid email or password")


class TokenExpiredError(AuthenticationError):
    """Raised when JWT token has expired."""

    def __init__(self) -> None:
        super().__init__(message="Token has expired")


class InvalidTokenError(AuthenticationError):
    """Raised when JWT token is malformed or invalid."""

    def __init__(self) -> None:
        super().__init__(message="Invalid or malformed token")


class InsufficientPermissionsError(AIBoardroomException):
    """Raised when user lacks required role/permissions."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message=message, status_code=403)


# ============================================================
# Resource Errors
# ============================================================
class NotFoundError(AIBoardroomException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource", resource_id: str | None = None) -> None:
        msg = f"{resource} not found"
        if resource_id:
            msg = f"{resource} with id '{resource_id}' not found"
        super().__init__(message=msg, status_code=404)


class DuplicateError(AIBoardroomException):
    """Raised when attempting to create a duplicate resource."""

    def __init__(self, resource: str = "Resource", field: str = "entry") -> None:
        super().__init__(
            message=f"{resource} with this {field} already exists",
            status_code=409,
        )


# ============================================================
# Validation Errors
# ============================================================
class ValidationError(AIBoardroomException):
    """Raised for input validation failures."""

    def __init__(self, message: str = "Validation error", detail: Any = None) -> None:
        super().__init__(message=message, status_code=422, detail=detail)


class FileValidationError(ValidationError):
    """Raised when an uploaded file fails validation."""

    def __init__(self, message: str = "Invalid file") -> None:
        super().__init__(message=message)


class FileSizeExceededError(FileValidationError):
    """Raised when file exceeds maximum size limit."""

    def __init__(self, max_size_mb: int = 50) -> None:
        super().__init__(message=f"File exceeds maximum size of {max_size_mb} MB")


class UnsupportedFileTypeError(FileValidationError):
    """Raised when file type is not supported."""

    def __init__(self, file_type: str = "") -> None:
        super().__init__(message=f"Unsupported file type: {file_type}")


# ============================================================
# AI & Agent Errors
# ============================================================
class AIProviderError(AIBoardroomException):
    """Raised when an AI provider returns an error."""

    def __init__(self, provider: str = "AI Provider", message: str = "Provider error") -> None:
        super().__init__(message=f"{provider}: {message}", status_code=502)


class AllProvidersFailedError(AIBoardroomException):
    """Raised when all AI providers fail (fallback exhausted)."""

    def __init__(self) -> None:
        super().__init__(
            message="All AI providers are unavailable. Please try again later.",
            status_code=503,
        )


class AgentExecutionError(AIBoardroomException):
    """Raised when an agent fails during execution."""

    def __init__(self, agent_name: str, message: str = "Agent execution failed") -> None:
        super().__init__(
            message=f"Agent '{agent_name}' failed: {message}",
            status_code=500,
        )


class OrchestratorError(AIBoardroomException):
    """Raised when the orchestrator workflow encounters an error."""

    def __init__(self, message: str = "Orchestration workflow failed") -> None:
        super().__init__(message=message, status_code=500)


# ============================================================
# Storage Errors
# ============================================================
class StorageError(AIBoardroomException):
    """Raised when file storage operations fail."""

    def __init__(self, message: str = "Storage operation failed") -> None:
        super().__init__(message=message, status_code=500)


class S3Error(StorageError):
    """Raised when S3 operations fail."""

    def __init__(self, message: str = "S3 operation failed") -> None:
        super().__init__(message=message)


# ============================================================
# Database Errors
# ============================================================
class DatabaseError(AIBoardroomException):
    """Raised when database operations fail."""

    def __init__(self, message: str = "Database operation failed") -> None:
        super().__init__(message=message, status_code=500)


# ============================================================
# Rate Limiting
# ============================================================
class RateLimitExceededError(AIBoardroomException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded. Please try again later.") -> None:
        super().__init__(message=message, status_code=429)


# ============================================================
# Report Errors
# ============================================================
class ReportGenerationError(AIBoardroomException):
    """Raised when report generation fails."""

    def __init__(self, report_type: str = "report", message: str = "Generation failed") -> None:
        super().__init__(
            message=f"Failed to generate {report_type}: {message}",
            status_code=500,
        )
