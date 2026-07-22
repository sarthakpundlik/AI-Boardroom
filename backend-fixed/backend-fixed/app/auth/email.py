"""
AI Boardroom — Email Service
Sends transactional emails like password resets.
"""

from __future__ import annotations

from email.message import EmailMessage

import aiosmtplib

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


async def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send an HTML email via SMTP."""
    settings = get_settings()

    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.warning("SMTP not configured, skipping email", to_email=to_email)
        return False

    message = EmailMessage()
    message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    message["To"] = to_email
    message["Subject"] = subject
    message.add_alternative(html_content, subtype="html")

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True,
        )
        logger.info("Email sent successfully", to_email=to_email, subject=subject)
        return True
    except Exception as e:
        logger.error("Failed to send email", to_email=to_email, error=str(e))
        return False


async def send_password_reset_email(to_email: str, reset_url: str) -> bool:
    """Send the password reset link to the user."""
    subject = "AI Boardroom — Password Reset"
    html_content = f"""
    <html>
        <body>
            <h2>Reset Your Password</h2>
            <p>You requested a password reset for your AI Boardroom account.</p>
            <p>Click the link below to reset your password. This link expires in 15 minutes.</p>
            <a href="{reset_url}" style="display:inline-block;padding:10px 20px;background:#2563EB;color:white;text-decoration:none;border-radius:5px;">Reset Password</a>
            <p>If you did not request this, please ignore this email.</p>
        </body>
    </html>
    """
    return await send_email(to_email, subject, html_content)
