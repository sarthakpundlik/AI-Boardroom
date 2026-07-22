"""
AI Boardroom — Auth Router
API endpoints for authentication, token management, and OAuth.
"""

from __future__ import annotations
from typing import Any

from fastapi import APIRouter, Depends, Header, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.email import send_password_reset_email
from app.auth.oauth import exchange_github_code, exchange_google_code, exchange_microsoft_code, get_github_user_info, get_google_user_info, get_microsoft_user_info
from app.auth.password import create_password_reset_token, verify_password_reset_token
from app.auth.schemas import (
    LoginRequest,
    OAuthCallbackRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from app.auth.service import AuthService
from app.auth.repository import AuthRepository
from app.core.config import get_settings
from app.core.constants import OAuthProvider
from app.core.dependencies import get_db
from app.core.exceptions import AuthenticationError, InvalidTokenError
from app.core.logging import get_logger
from app.users.schemas import UserCreate, UserResponse
from app.users.service import UserService

logger = get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    """Register a new user via email and password."""
    auth_service = AuthService(db)
    return await auth_service.register_user(data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    request: Request,
    user_agent: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Login with email and password to receive JWT tokens."""
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(data.email, data.password)
    
    # Track device/IP info
    device_info = f"{request.client.host if request.client else 'unknown'} | {user_agent or 'unknown'}"
    
    return await auth_service.create_tokens_for_user(user, device_info=device_info)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)) -> Any:
    """Get a new access token using a refresh token."""
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(data.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def logout(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)) -> None:
    """Revoke the current refresh token."""
    auth_service = AuthService(db)
    await auth_service.logout(data.refresh_token)


# --- OAuth 2.0 Routes ---

@router.post("/google/callback", response_model=TokenResponse)
async def google_callback(
    data: OAuthCallbackRequest,
    request: Request,
    user_agent: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Handle Google OAuth callback and exchange code for tokens."""
    auth_service = AuthService(db)
    access_token = await exchange_google_code(data.code)
    user_info = await get_google_user_info(access_token)
    
    user = await auth_service.handle_oauth_login(
        provider=OAuthProvider.GOOGLE,
        oauth_id=user_info["sub"],
        email=str(user_info.get("email", "")),
        name=str(user_info.get("name") or user_info.get("email") or ""),
        avatar_url=user_info.get("picture"),
    )
    
    device_info = f"{request.client.host if request.client else 'unknown'} | {user_agent or 'unknown'}"
    return await auth_service.create_tokens_for_user(user, device_info=device_info)


@router.post("/microsoft/callback", response_model=TokenResponse)
async def microsoft_callback(
    data: OAuthCallbackRequest,
    request: Request,
    user_agent: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Handle Microsoft OAuth callback and exchange code for tokens."""
    auth_service = AuthService(db)
    access_token = await exchange_microsoft_code(data.code)
    user_info = await get_microsoft_user_info(access_token)
    
    email = user_info.get("mail") or user_info.get("userPrincipalName")
    if not email:
        raise ValueError("Microsoft account has no email")
        
    user = await auth_service.handle_oauth_login(
        provider=OAuthProvider.MICROSOFT,
        oauth_id=user_info["id"],
        email=str(email),
        name=user_info.get("displayName", "Microsoft User"),
    )
    
    device_info = f"{request.client.host if request.client else 'unknown'} | {user_agent or 'unknown'}"
    return await auth_service.create_tokens_for_user(user, device_info=device_info)


@router.post("/github/callback", response_model=TokenResponse)
async def github_callback(
    data: OAuthCallbackRequest,
    request: Request,
    user_agent: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Handle GitHub OAuth callback and exchange code for tokens."""
    auth_service = AuthService(db)
    access_token = await exchange_github_code(data.code)
    user_info = await get_github_user_info(access_token)

    email = user_info.get("email", "")
    if not email:
        raise AuthenticationError("GitHub account has no verified email")

    user = await auth_service.handle_oauth_login(
        provider=OAuthProvider.GITHUB,
        oauth_id=str(user_info["id"]),
        email=str(email),
        name=user_info.get("name") or user_info.get("login", "GitHub User"),
        avatar_url=user_info.get("avatar_url"),
    )

    device_info = f"{request.client.host if request.client else 'unknown'} | {user_agent or 'unknown'}"
    return await auth_service.create_tokens_for_user(user, device_info=device_info)


# --- Password Reset Flow ---

@router.post("/password-reset-request", status_code=status.HTTP_202_ACCEPTED)
async def request_password_reset(data: PasswordResetRequest, db: AsyncSession = Depends(get_db)) -> Any:
    """Request a password reset email."""
    user_service = UserService(db)
    user = await user_service.get_user_by_email(data.email)
    
    if user and user.is_active:
        token = create_password_reset_token(user.email)
        settings = get_settings()
        # In a real app, this URL points to the frontend reset page
        reset_url = f"{settings.BACKEND_CORS_ORIGINS[0]}/auth/reset-password?token={token}"
        await send_password_reset_email(user.email, reset_url)
        
    # Always return 202 to prevent email enumeration
    return {"message": "If the email is registered, a reset link has been sent."}


@router.post("/password-reset-confirm", status_code=status.HTTP_200_OK)
async def confirm_password_reset(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)) -> Any:
    """Confirm password reset with the emailed token."""
    email = verify_password_reset_token(data.token)
    if not email:
        raise InvalidTokenError()
        
    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)
    if not user:
        raise InvalidTokenError()
        
    
    # We bypass the current password check here since they verified via email token
    # But we still use the service logic to validate strength and history
    # So we temporarily set a dummy request just to pass the new_password, 
    # but we'll manually implement the reset to avoid current_password check
    
    from app.core.security import hash_password, validate_password_strength, verify_password
    from app.core.exceptions import ValidationError
    
    errors = validate_password_strength(data.new_password)
    if errors:
        raise ValidationError("Password does not meet requirements", detail=errors)
        
    if user.password_history:
        past_hashes = user.password_history.split("|")
        for past_hash in past_hashes[-5:]:
            if verify_password(data.new_password, past_hash):
                raise ValidationError("Cannot reuse any of the last 5 passwords")
                
    new_hash = hash_password(data.new_password)
    old_history = user.password_history or ""
    user.password_history = f"{old_history}|{user.hashed_password}" if old_history else user.hashed_password
    user.hashed_password = new_hash
    
    await user_service.repo.update(user)
    
    # Revoke all existing sessions
    auth_repo = AuthRepository(db)
    await auth_repo.revoke_all_user_tokens(user.id)
    
    logger.info("Password reset successful", user_id=user.id)
    return {"message": "Password successfully reset"}
