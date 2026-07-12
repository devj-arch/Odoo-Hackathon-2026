import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def send_password_reset_email(to_email: str, reset_link: str) -> None:
    """
    Send a password reset email containing the reset link.

    Raises whatever exception smtplib raises on failure - callers can
    decide whether that should surface to the client or just be logged.
    """

    subject = "Reset your TransitOps password"

    body = (
        "We received a request to reset your TransitOps password.\n\n"
        f"Click the link below to choose a new password:\n{reset_link}\n\n"
        f"This link expires in {settings.RESET_TOKEN_EXPIRE_MINUTES} minutes. "
        "If you didn't request this, you can safely ignore this email."
    )

    message = MIMEMultipart()
    message["From"] = settings.SMTP_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        if settings.SMTP_USE_TLS:
            server.starttls()
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM, to_email, message.as_string())