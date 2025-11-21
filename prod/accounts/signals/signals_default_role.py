from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from accounts.models import Role  
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
       
        if not instance.role.exists():
            default_role = Role.objects.filter(permissions="Default").first()
            if default_role:
                instance.role.add(default_role)