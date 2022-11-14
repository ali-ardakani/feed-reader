from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser",
                                             email="test@test.com",
                                             password="testpassword")

    def test_register_user(self):
        data = {
            "username": "testuser1",
            "email": "test1@test.com",
            "password": "test1password"
        }
        response = self.client.post("/api/user/register/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "testuser1")
        self.assertEqual(response.data["email"], "test1@test.com")
        self.assertNotIn("password", response.data)

    def test_login_user(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post("/api/user/login/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "testuser")
        self.assertNotIn("password", response.data)
        self.assertIn("token", response.data)

    def test_wrong_login(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post("/api/user/login/", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["non_field_errors"][0],
                         "Incorrect Credentials")
