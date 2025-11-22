



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.api.views import UserViewSet , LogInView , SignUpView , ActivateAccountView , GoogleAuthInitView,GoogleAuthCallbackView , RefreshTokenView,LogoutView , ResetPassword , PasswordResetConfirmView

app_name = "accounts"


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router1 = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/' , LogInView.as_view() , name="login_view_api"),
    path('signup/' , SignUpView.as_view() , name="signup_view_api"),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    path("auth/google/init/", GoogleAuthInitView.as_view(), name="google-init"),
    path('auth/google/callback/', GoogleAuthCallbackView.as_view(), name='google-callback'),
    path('refresh-token/' , RefreshTokenView.as_view() , name="_refresh_token"),
    path('logout/' , LogoutView.as_view() , name="logout_refresh_token"),
    path('reset-password/' , ResetPassword.as_view() , name="reset-password"),
    path('reset-password/<uidb64>/<token>/' , PasswordResetConfirmView.as_view() , name="reset-password-activation")

]
