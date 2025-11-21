from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

class Role(models.Model):
    permissions = models.CharField(max_length=100,unique=True)
    level = models.PositiveIntegerField(default=999 , help_text="lower number means higher authority. CEO=1")
    group = models.ForeignKey(Group , on_delete=models.CASCADE , related_name="group_members" , null=True , blank=True)
    """Maps each role to specific system permissions."""
    content = models.ForeignKey(ContentType , on_delete=models.CASCADE , null=True , blank=True)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_view_all = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"


    def __str__(self):
        return f"{self.permissions} (L_{self.level}) , {self.content} under_{self.group}"