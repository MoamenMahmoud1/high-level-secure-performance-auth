from django.contrib.auth.base_user import BaseUserManager
from django.contrib.contenttypes.models import ContentType

class CustomUserManager(BaseUserManager):

    def create_user(self, email=None, password=None, role_name=None,  **extra_fields):
        from accounts.models import Role

        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)

        # إنشاء أو الحصول على Role
        if role_name:
            role = Role.objects.get(permissions=role_name)
        else:
            role, _ = Role.objects.get_or_create(permissions="Employee", defaults={"level": 999})



        user = self.model(email=email, **extra_fields)
        if password:
                user.set_password(password)

        user.save(using=self._db)
        user.role.set([role])
        user.save(using=self._db)
        



        return user


    def create_superuser(self, email, password=None, **extra_fields):
        from accounts.models import Role, CustomUserModel

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        user = self.create_user(email=email, password=password, **extra_fields)

        # ربط دور Admin
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(CustomUserModel)

        admin_role, _ = Role.objects.get_or_create(
            permissions="Admin",
            defaults={
                "level": 1,
                "content": content_type,
                "can_add": True,
                "can_edit": True,
                "can_view_all": True,
                "can_delete": True
            }
        )
        
        
        user.save(using=self._db)
        user.role.set([admin_role])
        user.save(using=self._db)

        return user
