from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from category.serializers import CategorySerializer
from tests.setup import setup_user


class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = setup_user()
        self.client.force_authenticate(user=self.user)

    def test_list_categories(self):
        Category.objects.create(name="Category 1", description="Description 1")
        Category.objects.create(name="Category 2", description="Description 2")

        response = self.client.get(reverse("categories-api"))
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], serializer.data)

    def test_create_category(self):
        data = {"name": "New Category", "description": "New Description"}
        response = self.client.post(reverse("categories-api"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "New Category")

    def test_update_category(self):
        category = Category.objects.create(name="Category", description="Description")
        updated_data = {
            "name": "Updated Category",
            "description": "Updated Description",
        }
        response = self.client.put(
            reverse("categories-api"),
            {"id": category.id, **updated_data},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, "Updated Category")
        self.assertEqual(category.description, "Updated Description")

    def test_delete_category(self):
        category = Category.objects.create(name="Category", description="Description")
        response = self.client.delete(
            reverse("categories-api"), data={"id": category.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
