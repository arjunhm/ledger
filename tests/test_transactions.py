from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests import setup
from transaction.models import Transaction


class TransactionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = setup.setup_user()
        self.client.force_authenticate(user=self.user)
        self.account = setup.setup_account()
        self.category = setup.setup_category()

    def test_list_transactions(self):
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            amount=100,
            type="income",
            date="2024-03-30",
        )
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            amount=50,
            type="expense",
            date="2024-03-29",
        )

        response = self.client.get(reverse("transactions-api"))
        transactions = Transaction.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("data", [])), transactions.count())

    def test_create_transaction(self):
        data = {
            "account": self.account.id,
            "category": self.category.id,
            "amount": 100,
            "type": "income",
            "date": "2024-03-30",
        }
        response = self.client.post(reverse("transactions-api"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().amount, 100)

    def test_retrieve_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account,
            amount=100,
            type="income",
            date="2024-03-30",
        )

        response = self.client.get(reverse("transactions-api"), {"id": transaction.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            txn_id = response.data.get("data", [])[0].get("id")
        except Exception:
            txn_id = -1
        self.assertEqual(txn_id, transaction.id)

    def test_update_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account,
            amount=100,
            type="income",
            date="2024-03-30",
        )
        updated_data = {
            "id": transaction.id,
            "account": self.account.id,
            "amount": 200,
            "type": "expense",
            "date": "2024-03-31",
        }

        response = self.client.put(
            reverse("transactions-api"),
            updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.type, "expense")

    def test_delete_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account,
            amount=100,
            type="income",
            date="2024-03-30",
        )
        response = self.client.delete(
            reverse("transactions-api"),
            {"id": transaction.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)
