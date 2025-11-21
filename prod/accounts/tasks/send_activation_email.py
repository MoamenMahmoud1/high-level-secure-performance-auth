from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging

logger = logging.getLogger(__name__)

# --------------------------
# Activation Email
# --------------------------
@shared_task(bind=True, max_retries=5)
def send_activation_email_task(self, user_id, username, user_email, token):
    """
    Send account activation email asynchronously.
    """
    try:
        uid = urlsafe_base64_encode(force_bytes(user_id))
        activate_url = f"{settings.FRONTEND_URL}/activate/{uid}/{token}"

        subject = "Activate your account"
        text_content = f"Hi {username},\nActivate your account:\n{activate_url}"
        html_content = render_to_string(
            "emails/activation_email.html",
            {"username": username, "activate_url": activate_url}
        )

        email = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_email]
        )
        email.attach_alternative(html_content, "text/html")
        logger.debug(f"Sending activation email to: {user_email}")
        email.send()

        return "Activation email sent"

    except Exception as exc:
        logger.error(f"Failed to send activation email to {user_email}: {exc}")
        raise self.retry(exc=exc, countdown=10)



# --------------------------
# Email Change Confirmation
# --------------------------
@shared_task(bind=True, max_retries=5)
def send_email_change_confirmation_task(self, username, old_email, new_email, token):
    """
    Send email change confirmation email asynchronously.
    """
    try:
        confirm_url = f"{settings.FRONTEND_URL}/confirm-email-change/{token}"

        subject = "Confirm Your Email Change"
        text_content = (
            f"Hi {username},\nConfirm your email change:\n{confirm_url}\n"
            f"Old email: {old_email}\nNew email: {new_email}"
        )
        html_content = render_to_string(
            "emails/email_change_confirmation.html",
            {"username": username, "old_email": old_email, "new_email": new_email, "confirm_url": confirm_url}
        )

        email = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, [new_email]
        )
        email.attach_alternative(html_content, "text/html")
        logger.debug(f"Sending email change confirmation to: {new_email}")
        email.send()

        return "Email change confirmation sent"

    except Exception as exc:
        logger.error(f"Failed to send email change confirmation to {new_email}: {exc}")
        raise self.retry(exc=exc, countdown=10)
