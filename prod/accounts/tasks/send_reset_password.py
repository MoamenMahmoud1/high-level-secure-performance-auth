from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging
logger = logging.getLogger(__name__)

# --------------------------
# Password Reset Email
# --------------------------
@shared_task(bind=True, max_retries=5)
def send_password_reset_email_task(self, user_id, username, user_email, token):
    """
    Send password reset email asynchronously.
    """
    try:
        uid = urlsafe_base64_encode(force_bytes(user_id))
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        subject = "Reset Your Password"
        text_content = f"Hi {username},\nReset your password:\n{reset_url}"
        html_content = render_to_string(
            "emails/password_reset_email.html",
            {"username": username, "reset_url": reset_url}
        )

        email = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_email]
        )
        email.attach_alternative(html_content, "text/html")
        logger.debug(f"Sending password reset email to: {user_email}")
        email.send()

        return "Password reset email sent"

    except Exception as exc:
        logger.error(f"Failed to send password reset email to {user_email}: {exc}")
        raise self.retry(exc=exc, countdown=10)