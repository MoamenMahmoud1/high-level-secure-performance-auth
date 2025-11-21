from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core import mail
from accounts.models import CustomUserModel

class TestPasswordResetRequest(APITestCase):

    def setUp(self):
        self.url = reverse("accounts:reset-password")
        CustomUserModel.objects.create_user(username="test",email="reset@test.com", password="1234" , is_active=True , is_verified=True)

    def test_reset_password_email_sent(self):
        data = {"email": "reset@test.com"}
        res = self.client.post(self.url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
