from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class CookieJWTAuthentication(BaseAuthentication):
    """
    Read access token
    """
    def authenticate(self, request):

        active_user_id = request.headers.get("X-Active-User")

        if not active_user_id:
            return None

        cookie_name = f"access_token_{active_user_id}"
        token = request.COOKIES.get(cookie_name)

        if not token:
            return None

        try:
            validated = AccessToken(token)
            user = User.objects.get(id=validated["user_id"])
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        return (user, validated)
