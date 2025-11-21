from django.contrib import admin 
from accounts.models import CustomUserModel  , Role
# Register your models here.

@admin.register(CustomUserModel)
class Custom(admin.ModelAdmin):
    pass

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass
