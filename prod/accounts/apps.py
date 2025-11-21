from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'





    def ready(self):
        from accounts.signals import assign_default_role
        from accounts.signals import clear_role_cache
        
        
