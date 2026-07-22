"""
AI Boardroom — Auth Service
Business logic for login, registration, tokens, and OAuth flows.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_refresh_token
from app.auth.repository import AuthRepository
from app.core.config import get_settings
from app.core.constants import OAuthProvider
from app.core.exceptions import AuthenticationError, InvalidCredentialsError, InvalidTokenError, TokenExpiredError
from app.core.logging import get_logger
from app.core.security import hash_password, verify_password
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreate

logger = get_logger(__name__)


class AuthService:
    """Service layer for authentication."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.auth_repo = AuthRepository(session)
        self.user_repo = UserRepository(session)

    async def authenticate_user(self, email: str, password: str) -> User:
        """Validate email and password."""
        user = await self.user_repo.get_by_email(email)
        if not user or not user.hashed_password:
            raise InvalidCredentialsError()
            
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
            
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")
            
        return user

    async def register_user(self, data: UserCreate) -> User:
        """Register a new user via email."""
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            # Prevent leaking user existence directly, but for APIs a 409 is common
            raise AuthenticationError("Email already registered")
            
        user = User(
            email=data.email,
            name=data.name,
            hashed_password=hash_password(data.password),
            oauth_provider=OAuthProvider.EMAIL,
        )
        return await self.user_repo.create(user)

    async def create_tokens_for_user(self, user: User, device_info: str | None = None) -> dict:
        """Generate access and refresh tokens for a user."""
        settings = get_settings()
        
        # Access token
        access_token = create_access_token({"sub": user.id, "role": user.role})
        
        # Refresh token
        refresh_token_str = create_refresh_token({"sub": user.id})
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Store refresh token in DB
        await self.auth_repo.create_refresh_token(
            user_id=user.id,
            token=refresh_token_str,
            expires_at=expires_at,
            device_info=device_info,
        )
        
        # Update last login
        await self.user_repo.update_last_login(user)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str,
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """Generate a new access token using a valid refresh token."""
        payload = decode_refresh_token(refresh_token)
        if not payload:
            raise InvalidTokenError()
            
        user_id = payload.get("sub")
        if not isinstance(user_id, str):
            raise InvalidTokenError()
        
        # Check if token is revoked in DB
        db_token = await self.auth_repo.get_refresh_token(refresh_token)
        if not db_token:
            raise InvalidTokenError()
            
        if db_token.is_revoked:
            logger.warning("Attempted to use revoked refresh token", user_id=user_id)
            # Security measure: if a revoked token is used, revoke ALL tokens for user
            await self.auth_repo.revoke_all_user_tokens(user_id)
            raise InvalidTokenError()
            
        if db_token.expires_at < datetime.now(timezone.utc):
            raise TokenExpiredError()
            
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
            
        # Rotate refresh token (revoke old, create new)
        await self.auth_repo.revoke_refresh_token(refresh_token)
        return await self.create_tokens_for_user(user, db_token.device_info)

    async def logout(self, refresh_token: str) -> None:
        """Revoke a specific refresh token."""
        await self.auth_repo.revoke_refresh_token(refresh_token)

    async def handle_oauth_login(self, provider: str, oauth_id: str, email: str, name: str, avatar_url: str | None = None) -> User:
        """Handle login or registration via OAuth provider."""
        # 1. Try to find user by OAuth ID
        user = await self.user_repo.get_by_oauth(provider, oauth_id)
        
        # 2. If not found, check by email to link accounts
        if not user:
            user = await self.user_repo.get_by_email(email)
            if user:
                # Link OAuth to existing account
                user.oauth_provider = provider
                user.oauth_id = oauth_id
                if not user.avatar_url and avatar_url:
                    user.avatar_url = avatar_url
                await self.user_repo.update(user)
                
        # 3. If still not found, create new user
        if not user:
            user = User(
                email=email,
                name=name,
                oauth_provider=provider,
                oauth_id=oauth_id,
                avatar_url=avatar_url,
            )
            user = await self.user_repo.create(user)
            
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")
            
        return user
