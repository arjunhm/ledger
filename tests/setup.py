from django.contrib.auth import get_user_model

from account.models import Account
from category.models import Category


def setup_user(email="testuser@gmail.com", password="1234"):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return User.objects.create_user(email=email, password=password)


def setup_category():
    return Category.objects.create(name="Category 1", description="Description 1")


def setup_account():
    user = setup_user()
    return Account.objects.create(
        user=user, name="Test Account", account_type="checking"
    )
