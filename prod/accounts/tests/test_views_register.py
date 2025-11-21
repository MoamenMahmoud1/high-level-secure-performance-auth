from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUserModel

class TestRegister(APITestCase):

    def setUp(self):
        self.url = reverse("accounts:signup_view_api_refresh_token")

    def test_register_success(self):
        data = {"username":"Test","email": "ok@test.com","first_name":"test" , "last_name":"testname","password": "12345678" , "password2":"12345678"}
        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUserModel.objects.filter(email=data["email"]).exists())

    def test_register_existing_email(self):
        CustomUserModel.objects.create_user(email="user@test.com", password="1234")
        data = {"username":"Test","email": "ok@test","first_name":"test" , "last_name":"testname","password": "12345678" , "password2":"12345678"}
        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
