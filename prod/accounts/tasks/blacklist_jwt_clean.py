from celery import shared_task
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from datetime import datetime

@shared_task
def cleanup_blacklisted_tokens():
    """
    Deleted the blacklist tokens
    """
    now = datetime.now()
    expired_tokens = BlacklistedToken.objects.filter(
        token__expires_at__lt=now
    )
    count = expired_tokens.count()
    expired_tokens.delete()
    return f"Deleted {count} expired blacklisted tokens"
