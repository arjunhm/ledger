from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from tests.setup import setup_user


class AuthenticationAPITest(TestCase):
    def setUp(self):
        self.user = setup_user(email="test@example.com", password="password")

    def test_login_success(self):
        data = {"email": "test@example.com", "password": "password"}
        response = self.client.post(reverse("login-api"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        data = {"email": "test@example.com", "password": "wrong_password"}
        response = self.client.post(reverse("login-api"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout-api"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_not_authenticated(self):
        response = self.client.post(reverse("logout-api"), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
