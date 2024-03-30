from django.contrib.auth import get_user_model


def setup_user():
    User = get_user_model()
    user = User.objects.create_user(email="testuser", password="12345")
    return user
