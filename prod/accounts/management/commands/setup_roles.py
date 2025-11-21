# setup_roles.py
from django.core.management.base import BaseCommand
from accounts.models import Department, Role
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = "Setup default departments and roles"

    def handle(self, *args, **options):
        departments = ["HR", "IT", "Finance", "Operations"]
        for dept_name in departments:
            department, created = Department.objects.get_or_create(name=dept_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Department created: {dept_name}"))

            # ContentType for user model
            user_ct = ContentType.objects.get(app_label='accounts', model='customusermodel')

            # Roles
            roles_data = [
                {"permissions": "Manager", "level": 2, "content": user_ct},
                {"permissions": "Employee", "level": 999, "content": user_ct},
            ]
            for role_data in roles_data:
                role, created = Role.objects.get_or_create(
                    permissions=role_data["permissions"],
                    defaults={
                        "level": role_data["level"],
                        "department": department,
                        "content": role_data["content"],
                        "can_add": True if role_data["permissions"] == "Manager" else False,
                        "can_edit": True if role_data["permissions"] == "Manager" else False,
                        "can_view_all": True if role_data["permissions"] == "Manager" else False,
                        "can_delete": True if role_data["permissions"] == "Manager" else False,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Role '{role.permissions}' created for Department '{department.name}'"
                    ))
