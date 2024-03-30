from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password"
        )

    def test_get_user_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_unauthenticated(self):
        url = reverse("user-api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user(self):
        url = reverse("user-api")
        data = {
            "email": "newuser@example.com",
            "password": "password",
            "password2": "password",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_create_user_password_mismatch(self):
        url = reverse("user-api")
        data = {
            "email": "newuser@example.com",
            "password": "password",
            "password2": "password123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="newuser@example.com").exists())

    def test_create_user_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-api")
        data = {
            "email": "newuser@example.com",
            "password": "password",
            "password2": "password",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-api")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_delete_user_unauthenticated(self):
        url = reverse("user-api")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reset_password(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("reset-password-api")
        data = {"password": "newpassword", "password2": "newpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword"))

    def test_reset_password_password_mismatch(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("reset-password-api")
        data = {"password": "newpassword", "password2": "newpassword123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("newpassword123"))

    def test_reset_password_unauthenticated(self):
        url = reverse("reset-password-api")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
