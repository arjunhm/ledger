from django.contrib.auth import get_user_model
from category.models import Category
from account.models import Account


def setup_user():
    User = get_user_model()
    try:
        user = User.objects.get(email="testuser")
        return user
    except User.DoesNotExist:
        return User.objects.create_user(email="testuser", password="12345")


def setup_category():
    return Category.objects.create(name="Category 1", description="Description 1")


def setup_account():
    user = setup_user()
    return Account.objects.create(
        user=user, name="Test Account", account_type="checking"
    )
