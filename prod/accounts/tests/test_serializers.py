from django.test import TestCase
from accounts.api.serializers import SignUpSer

class TestRegisterSerializer(TestCase):

    def test_valid_data(self):
        data = {"username":"Test","email": "ok@test.com","first_name":"test" , "last_name":"testname","password": "12345678" , "password2":"12345678"}
        serializer = SignUpSer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        data = {"username":"Test","email": "ok@test", "password": "12345678" , "password2":"12345678","first_name":"test" , "last_name":"testname"}
        serializer = SignUpSer(data=data)
        self.assertFalse(serializer.is_valid())


