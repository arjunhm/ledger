from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from account.models import Account
from account.serializers import AccountSerializer
from django.contrib.auth import get_user_model


class AccountAPITest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client = APIClient()
        self.user = User.objects.create_user(email="testuser", password="12345")
        self.client.force_authenticate(user=self.user)

    def test_list_accounts(self):
        Account.objects.create(
            user=self.user,
            name="Test Account 1",
            account_type="savings",
            balance=1000.00,
        )
        Account.objects.create(
            user=self.user,
            name="Test Account 2",
            account_type="Checking",
            balance=500.00,
        )

        response = self.client.get(reverse("account-api"))
        accounts = Account.objects.filter(user=self.user)
        serializer = AccountSerializer(accounts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], serializer.data)

    def test_create_account(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "New Account", "account_type": "savings", "balance": 2000.00}
        response = self.client.post(reverse("account-api"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, "New Account")

    def test_update_account(self):
        self.client.force_authenticate(user=self.user)
        account = Account.objects.create(
            user=self.user, name="Test Account", account_type="savings", balance=1000.00
        )
        updated_data = {"name": "Updated Account", "balance": 1500.00, "account_type": account.account_type}
        response = self.client.put(
            reverse("account-api"), {"id": account.id, **updated_data}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account.refresh_from_db()
        self.assertEqual(account.name, "Updated Account")
        self.assertEqual(account.balance, 1500.00)

    def test_delete_account(self):
        self.client.force_authenticate(user=self.user)
        account = Account.objects.create(
            user=self.user, name="Test Account", account_type="savings", balance=1000.00
        )
        response = self.client.delete(reverse("account-api"), {"id": account.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)
