import logging
import uuid
import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication 
from accounts.models import CustomUserModel
from .serializers import UserSerializer, SignUpSer, LogInSerializer , ResetSerializer , PasswordSerializer
from common.permissions import RoleBasePermission
from authentication import activation_token_generator , password_reset_token
from authentication import EncryptedRefreshToken
from common.pagination import UserPagination
from django.core.cache import cache
from accounts.models import Role
from django.db.models import Prefetch , Case , When , BooleanField
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)
User = CustomUserModel

# ===============================
# User CRUD operations using DRF ModelViewSet
# Handles permissions, queryset optimization, and pagination
# ===============================
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [RoleBasePermission]
    pagination_class = UserPagination
    queryset = CustomUserModel.objects.none()
    
    def get_queryset(self):
        user = self.request.user

        # Superuser receives full dataset
        if user.is_superuser:
            return CustomUserModel.objects.all().select_related('manager').prefetch_related(
                Prefetch('role', queryset=Role.objects.all())
            )

        # Annotate current user to appear first in the list
        qs = CustomUserModel.objects.all().select_related('manager').prefetch_related(
            Prefetch('role', queryset=Role.objects.all())
        ).annotate(
            is_current_user=Case(
                When(pk=user.pk, then=True),
                default=False,
                output_field=BooleanField()
            )
        ).order_by('-is_current_user', 'username')  # current user first

        # Defer sensitive fields for other users
        qs = qs.defer('password', 'email')
        return qs
    
    def create(self, request, *args, **kwargs):
        # Create user using serializer
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        logger.debug(f"Created user {result.get('user')}")
        return Response(result, status=status.HTTP_201_CREATED)


# ===============================
# Sign-up endpoint
# Handles user registration, sets HttpOnly cookies with JWT tokens
# ===============================
class SignUpView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = SignUpSer

    def post(self, request):
        serializer = SignUpSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        user = result["user"]
        token = result["token"]
        refresh = result["refresh"]
        uid = user.pk
        logger.debug(f"uid is a {uid}")

        response = Response({"detail": f"User created with id_{uid}"}, status=status.HTTP_201_CREATED)

        # Set HttpOnly cookies for JWT access and refresh tokens
        response.set_cookie(key=f"access_token_{uid}", value=str(token))
        response.set_cookie(key=f"refresh_token_{uid}", value=str(refresh))

        logger.debug(f"Signup completed for user id {uid}")
        return response


# ===============================
# Login endpoint
# Authenticates user and sets JWT tokens in HttpOnly cookies
# ===============================
class LogInView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = LogInSerializer

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = serializer.validated_data["token"]
        refresh = serializer.validated_data["refresh"]
        uid = user.id

        response = Response({
            "detail": "Logged in successfully",
            "user_id": uid,
        }, status=status.HTTP_200_OK)

        # Set HttpOnly cookies
        response.set_cookie(key=f"access_token_{uid}", value=str(token))
        response.set_cookie(key=f"refresh_token_{uid}", value=str(refresh))

        logger.debug(f"User {uid} logged in successfully")
        return response


# ===============================
# Account activation endpoint
# Validates activation token and marks account as active
# ===============================
class ActivateAccountView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token , first_time=True):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):
            logger.warning("Invalid activation link attempt")
            return Response({"detail": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)

        if activation_token_generator.check_token(user, token) and first_time:
            user.is_active = True
            user.is_verfied = True
            user.save()
            logger.debug(f"User {uid} activated successfully")
            return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Invalid or expired activation token for user {uid}")
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


# ===============================
# Google OAuth initiation
# Generates Google login URL with CSRF protection state
# ===============================
class GoogleAuthInitView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def get(self, request):
        state = str(uuid.uuid4())
        request.session['google_auth_state'] = state
        logger.debug(f"Generated state: {state}")
        logger.debug(f"Session after setting state: {request.session.items()}")
        google_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=openid email profile&"
            f"state={state}"
        )
        return Response({"url": google_url})


# ===============================
# Google OAuth callback
# Exchanges authorization code for tokens, creates/updates user
# ===============================
class GoogleAuthCallbackView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        state = request.query_params.get('state')
        session_state = request.session.get('google_auth_state')

        logger.debug(f"State from Google callback: {state}")
        logger.debug(f"State from session: {session_state}")

        # CSRF protection: state must match
        if state != session_state:
            logger.warning("State mismatch in Google callback")
            return Response({"error": "Invalid state"}, status=400)

        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_res = requests.post(token_url, data=data).json()
        logger.debug(f"Token response: {token_res}")

        access_token = token_res.get('access_token')

        # Retrieve user info from Google
        user_info_res = requests.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()
        logger.debug(f"Full Google user info: {user_info_res}")

        email = user_info_res.get('email')
        if not email:
            logger.warning("Google account did not provide email")
            return Response({"error": "Email not provided by Google"}, status=400)

        first_name = user_info_res.get('given_name')
        last_name = user_info_res.get('family_name')

        # Create or update user
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.first_name = first_name
            user.last_name = last_name
            user.set_unusable_password()
            user.is_active = True
            user.save()
            logger.debug(f"New user created from Google login: {email}")

        # Generate JWT tokens
        refresh = EncryptedRefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({
            "message": "Login successful",
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        })
        uid = user.id
        # Set HttpOnly cookies
        response.set_cookie(key=f"access_token_{uid}", value=str(access), httponly=True, secure=True, samesite="None")
        response.set_cookie(key=f"refresh_token_{uid}", value=str(refresh), httponly=True, secure=True, samesite="None")

        logger.debug(f"Google login completed for user {email}")
        return response


# ===============================
# Refresh token endpoint
# Handles refreshing JWT access tokens using refresh token cookie
# ===============================
@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def post(self, request):
        active_user_id = request.headers.get("X-Active-User")
        if not active_user_id:
            logger.warning("Missing X-Active-User header on token refresh")
            return Response({"error": "Missing X-Active-User"}, status=400)

        refresh_token = request.refresh_token_decrypted
        logger.debug(f"refresh_token: {refresh_token}")

        if not refresh_token:
            logger.warning(f"No refresh token found for user {active_user_id}")
            return Response({"error": "No refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = EncryptedRefreshToken(refresh_token)
            new_access = refresh.access_token
        except TokenError:
            logger.warning(f"Invalid refresh token for user {active_user_id}")
            return Response({"error": "Invalid refresh"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "Token refreshed"}, status=200)
        response.set_cookie(key=f"access_token_{active_user_id}", value=str(new_access))
        logger.debug(f"Access token refreshed for user {active_user_id}")
        return response


# ===============================
# Logout endpoint
# Blacklists refresh token and deletes cookies
# ===============================
class LogoutView(APIView):
    def post(self, request):
        active_user_id = request.headers.get("X-Active-User")
        if not active_user_id:
            logger.warning("Missing X-Active-User header on logout")
            return Response({"error": "Missing X-Active-User header"}, status=400)

        refresh_token = request.refresh_token_decrypted

        if refresh_token:
            try:
                token = EncryptedRefreshToken(refresh_token)
                token.blacklist()
                logger.debug(f"Refresh token blacklisted for user {active_user_id}")
            except TokenError:
                logger.warning(f"Refresh token invalid or expired for user {active_user_id}")

        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie(f"access_token_{active_user_id}")
        response.delete_cookie(f"refresh_token_{active_user_id}")

        logger.debug(f"User {active_user_id} logged out successfully")
        return response


# ===============================
# Password reset initiation endpoint
# Sends reset link via email
# ===============================
class ResetPassword(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetSerializer

    def post(self, request):
        serializer = ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail":"Password reset link sent"}, status=status.HTTP_200_OK)


# ===============================
# Confirm password reset endpoint
# Validates token and updates user password
# ===============================
class PasswordResetConfirmView(APIView):
    serializer_class = PasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        new_password = PasswordSerializer(data=request.data)
        new_password.is_valid(raise_exception=True)
        password = new_password.validated_data['password']
        if not new_password:
            return Response({"error": "New password required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):
            logger.warning("Invalid password reset link attempt")
            return Response({"detail": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        if not password_reset_token.check_token(user, token):
            logger.warning(f"Invalid or expired reset token for user {uid}")
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        logger.debug(f"Password reset successful for user {uid}")

        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
