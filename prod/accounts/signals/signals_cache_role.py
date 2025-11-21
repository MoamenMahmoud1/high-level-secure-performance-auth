from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from accounts.models import Role
from django.core.cache import cache

@receiver(post_save , sender=Role)
@receiver(post_delete , sender=Role)
def clear_role_cache(sender , instance , **kwargs):
    cache.delete(f"role:{instance.id}")
