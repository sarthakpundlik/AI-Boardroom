"""
AI Boardroom — OAuth Clients
Integration with Google and Microsoft OAuth 2.0.
"""

from __future__ import annotations

import httpx

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.logging import get_logger

logger = get_logger(__name__)


async def get_google_user_info(access_token: str) -> dict:
    """Fetch user profile from Google using the OAuth access token."""
    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
    if response.status_code != 200:
        logger.error("Google OAuth failed", status=response.status_code, body=response.text)
        raise AuthenticationError("Failed to fetch user profile from Google")
        
    return response.json()


async def get_microsoft_user_info(access_token: str) -> dict:
    """Fetch user profile from Microsoft using the OAuth access token."""
    url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
    if response.status_code != 200:
        logger.error("Microsoft OAuth failed", status=response.status_code, body=response.text)
        raise AuthenticationError("Failed to fetch user profile from Microsoft")
        
    return response.json()


async def exchange_google_code(code: str) -> str:
    """Exchange authorization code for an access token."""
    settings = get_settings()
    url = "https://oauth2.googleapis.com/token"
    
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        
    if response.status_code != 200:
        logger.error("Google token exchange failed", body=response.text)
        raise AuthenticationError("OAuth token exchange failed")
        
    return response.json()["access_token"]


async def exchange_microsoft_code(code: str) -> str:
    """Exchange authorization code for an access token."""
    settings = get_settings()
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    
    data = {
        "client_id": settings.MICROSOFT_CLIENT_ID,
        "client_secret": settings.MICROSOFT_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        
    if response.status_code != 200:
        logger.error("Microsoft token exchange failed", body=response.text)
        raise AuthenticationError("OAuth token exchange failed")
        
    return response.json()["access_token"]


async def get_github_user_info(access_token: str) -> dict:
    """Fetch user profile from GitHub using the OAuth access token."""
    url = "https://api.github.com/user"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        logger.error("GitHub OAuth failed", status=response.status_code, body=response.text)
        raise AuthenticationError("Failed to fetch user profile from GitHub")

    data = response.json()

    # GitHub may not return an email if the user's email is private.
    # In that case, hit the /user/emails endpoint to get the primary email.
    if not data.get("email"):
        async with httpx.AsyncClient() as client:
            emails_resp = await client.get(
                "https://api.github.com/user/emails", headers=headers
            )
        if emails_resp.status_code == 200:
            for entry in emails_resp.json():
                if entry.get("primary") and entry.get("verified"):
                    data["email"] = entry["email"]
                    break

    return data


async def exchange_github_code(code: str) -> str:
    """Exchange GitHub authorization code for an access token."""
    settings = get_settings()
    url = "https://github.com/login/oauth/access_token"

    data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, data=data, headers={"Accept": "application/json"}
        )

    if response.status_code != 200:
        logger.error("GitHub token exchange failed", body=response.text)
        raise AuthenticationError("OAuth token exchange failed")

    body = response.json()
    if "error" in body:
        logger.error("GitHub token exchange error", error=body)
        raise AuthenticationError(body.get("error_description", "OAuth token exchange failed"))

    return body["access_token"]
