import logging
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate
from authentication import EncryptedRefreshToken
from accounts.tasks import send_activation_email_task, send_password_reset_email_task

from accounts.models import CustomUserModel, Role 
from authentication.tokens_activate import activation_token_generator, password_reset_token

logger = logging.getLogger(__name__)

# ===============================
# Serializer for user sign-up
# Handles user creation, password validation, and sending activation email asynchronously
# ===============================
class SignUpSer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Ensure password and password2 match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords didn't match")
        return data

    def create(self, validated_data):
        # Remove redundant password2 before creating user
        validated_data.pop("password2")
        # Create user in database
        user = CustomUserModel.objects.create_user(**validated_data)
        # Generate activation token
        token = activation_token_generator.make_token(user)
        # Send activation email asynchronously
        send_activation_email_task.delay(user.pk, user.username, user.email, token)
        # Generate refresh and access token for immediate login
        refresh = EncryptedRefreshToken.for_user(user)
        logger.debug(f"User created: {user.username} , {user.pk}")
        return {
            'user': user,
            'refresh': refresh,
            'token': refresh.access_token,
        }


# ===============================
# Serializer for Role model
# Used to display role info like permissions and level
# ===============================
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'permissions', 'level']


# ===============================
# Serializer for User model
# Handles create/update, role assignment, and controlled output depending on requesting user
# ===============================
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    role = serializers.SerializerMethodField()
    role_id = serializers.PrimaryKeyRelatedField(
        source='role',
        queryset=Role.objects.all(),
        write_only=True,
        required=False,
        many=True
    )

    class Meta:
        model = CustomUserModel
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password2', 'role', 'is_active',
            'is_verified', 'role_id'
        ]
        read_only_fields = ['is_active', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def get_role(self, obj):
        # Serialize roles assigned to user
        roles = obj.role.all()
        return RoleSerializer(roles, many=True).data

    def to_representation(self, instance):
        # Limit visible fields for non-superusers when viewing other users
        user = self.context['request'].user
        data = super().to_representation(instance)
        if not user.is_superuser and user != instance:
            allowed = ['username', 'first_name', 'last_name', 'role']
            data = {k: v for k, v in data.items() if k in allowed}
        return data

    def validate(self, data):
        # Ensure password confirmation
        if data.get('password') != data.get('password2'):
            raise ValidationError("Passwords didn't match")
        return data

    def create(self, validated_data):
        # Remove redundant password2
        validated_data.pop('password2', None)
        roles = validated_data.pop('role', None)

        # Assign default role if none provided
        if not roles:
            roles = Role.objects.filter(permissions="Employee")

        user = CustomUserModel.objects.create_user(**validated_data)
        if roles:
            user.role.set([roles])
        user.save()

        refresh = EncryptedRefreshToken.for_user(user)
        logger.debug(f"User created: {user.username} | Roles: {[r.permissions for r in roles]}")
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': [r.permissions for r in roles],
                'is_active': user.is_active,
                'is_verified': user.is_verified,
            },
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }

    def update(self, instance, validated_data):
        # Update user fields and roles if provided
        roles = validated_data.pop('role', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if roles:
            instance.role.set(roles)
        instance.save()
        logger.debug(f"User updated: {instance.username}")
        return instance


# ===============================
# Serializer for login
# Handles username/email authentication and JWT token generation
# ===============================
class LogInSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get("username_or_email")
        password = data.get("password")

        # Authenticate user using username
        user = authenticate(username=username_or_email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or email")
        if not user.is_active:
            raise serializers.ValidationError("Incorrect password or inactive user")

        refresh = EncryptedRefreshToken.for_user(user)
        access_token = refresh.access_token
        enc = refresh.encrypt()
        logger.debug(f"User logged in: {user.username}")
        return {
            'user': user,
            'refresh': str(enc),
            'token': str(access_token),
        }


# ===============================
# Serializer for password reset
# Validates email, fetches user, and sends reset email asynchronously
# ===============================
class ResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, data):
        obj_wanted = data.get("email")
        user = CustomUserModel.objects.filter(email=obj_wanted).last()
        if not user:
            raise serializers.ValidationError({"email": "Email not found"})
        if not user.is_active:
            raise serializers.ValidationError({"email": "Email not active"})
        self.user = user
        return data

    def create(self, validated_data):
        # Generate password reset token and send reset email asynchronously
        token = password_reset_token.make_token(self.user)
        send_password_reset_email_task.delay(self.user.pk, self.user.username, self.user.email, token)
        return self.user


# ===============================
# Serializer for password update
# ===============================
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
