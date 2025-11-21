from django.db import models
from django.conf import settings

from managers.user_manager import CustomUserManager

from django.utils import timezone

from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


#from accounts.models.role import Role


from django.contrib.contenttypes.models import ContentType
class CustomUserModel(AbstractUser):

    username = models.CharField(max_length=20 , unique=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    phone_number = PhoneNumberField(default="" , blank=True , null=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    role = models.ManyToManyField("accounts.Role" , blank=True)
    
    manager = models.ForeignKey('self' , on_delete=models.SET_NULL , null=True , blank=True , related_name="team_members" , help_text="Direct manager for this employee")
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()
    photo = models.ImageField(upload_to="photo/%y/%m/%d/" , null=True , blank=True)
    password_time_edited = models.DateTimeField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True , blank=True)
    updated_at = models.DateTimeField(auto_now=True , null=True , blank=True)
    



    def set_password(self, raw_password):
        super().set_password(raw_password)
        self.password_time_edited = timezone.now()
        
    

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        #ordering = ["email"]
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            #models.Index(fields=['is_active']),
            #models.Index(fields=['manager']),
            #models.Index(fields=['is_active', 'manager']),  # لو كتير بتفلتر على الاثنين مع بعض
            ]   

    def __str__(self):
        return f"{self.username} with {self.email}"
    
    #@property
    #def is_manager(self):
    #    return self.role and self.role.level <= 3
    #
#
    #@property
    #def permissions(self):
    #    """Shortcut للوصول لصلاحيات الدور المرتبطة بالموديل الحالي."""
    #    if not self.role:
    #        return None
    #    ct = ContentType.objects.get_for_model(self.__class__)
    #    return getattr(self.role, "permissions", None) if getattr(self.role, "permissions", None) and getattr(self.role, "content", None) == ct else None





