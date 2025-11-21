from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUserModel
from authentication.tokens_activate import activation_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class TestActivation(APITestCase):

    def test_activation_success(self):
        user = CustomUserModel.objects.create_user(
            email="activate@test.com", password="12345678", is_active=False
        )
        token = activation_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        url = reverse("accounts:activate_refresh_token", kwargs={"uidb64": uid, "token": token})
        res = self.client.get(url)

        user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(user.is_active)
