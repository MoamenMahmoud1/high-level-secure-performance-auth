from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUserModel

@shared_task
def delete_inactive_users_after_30_days():
    cutoff_date = timezone.now() - timedelta(days=30)
    users = CustomUserModel.objects.filter(is_active=False, date_joined__lt=cutoff_date)
    
    count = users.count()
    users.delete()
    return f"Deleted {count} inactive users older than 30 days"
