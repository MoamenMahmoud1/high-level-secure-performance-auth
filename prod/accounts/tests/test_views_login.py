from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUserModel

class TestLogin(APITestCase):

    def setUp(self):
        self.url = reverse("accounts:login_view_api_refresh_token")
        self.user = CustomUserModel.objects.create_user(username="test",
            email="test@test.com", password="12345678", is_active=True,is_verified=True)

    def test_login_success(self):
        data = {"username_or_email": "test@test.com", "password": "12345678"}
        res = self.client.post(self.url, data)
        uid = self.user.id
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(f"refresh_token_{uid}", res.cookies)
        self.assertIn(f"access_token_{uid}", res.cookies)

    def test_login_wrong_password(self):
        data = {"username_or_email": "test@test.com", "password": "wrongpass"}
        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
