from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.contenttypes.models import ContentType
from accounts.models.role import Role
import logging    

from django.contrib.auth.models import Group


logger = logging.getLogger(__name__)
logger.debug("Checking permission…")





from django.core.cache import cache
class RoleBasePermission(BasePermission):

    """Permission based on user role, group, and object hierarchy"""

    def get_role_cached(self, role_id):
        """ Make cache to increase performance"""
        cache_key = f"role:{role_id}"
        role_data = cache.get(cache_key)
        if role_data is None:
            role = Role.objects.get(id=role_id)
            role_data = {
                "id": role.id,
                "can_view_all": role.can_view_all,
                "can_add": role.can_add,
                "can_edit": role.can_edit,
                "can_delete": role.can_delete,
                "content_id": role.content_id,
                "level": role.level
            }
            cache.set(cache_key, role_data, timeout=600)
            logger.debug("Role cached: %s", role.id)
        return role_data

    def has_permission(self, request, view):
        user = request.user
        logger.debug("Checking permission for: %s", getattr(user, "username", "Anonymous"))
        logger.debug("Authenticated: %s", user.is_authenticated)
        logger.debug("Superuser: %s", user.is_superuser)

        if request.method == "OPTIONS":
            return True

        if user.is_superuser:
            return True

        if not user.is_authenticated or not user.role.exists():
            return False

        queryset = getattr(view, "queryset", None)
        if queryset is None:
            return False

        model_class = queryset.model
        ct_id = ContentType.objects.get_for_model(model_class).id

        # جلب roles من cache
        role_ids = list(user.role.values_list("id", flat=True))
        roles = [self.get_role_cached(rid) for rid in role_ids]

        for role in roles:
            if role["content_id"] != ct_id:
                continue

            if request.method == "GET" and role["can_view_all"]:
                return True

            if request.method == "POST" and role["can_add"]:
                data = request.data.get("role_id")
                if not data:
                    return False
                else:
                    try:
                        new_role = self.get_role_cached(int(data))
                        if new_role["level"] > role["level"]:
                            return True
                    except Role.DoesNotExist:
                        continue

            if request.method in ["PUT", "PATCH"] and role["can_edit"]:
                return True

            if request.method == "DELETE" and role["can_delete"]:
                return True
        return False
        

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True

        under_manager = self.is_under_manager(user, obj)

        # GET -> السماح لأي user يشوف التفاصيل
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # PUT/PATCH/DELETE -> لازم يكون تحت المدير
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return under_manager

        return False


        

    @staticmethod
    def is_under_manager(user, obj):
        manager = getattr(obj, "manager", None)
        while manager is not None:
            if manager == user:
                return True
            manager = getattr(manager, "manager", None)
        return False