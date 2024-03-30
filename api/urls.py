from django.urls import path
from api.views import (
    user_views,
    account_views,
    category_views,
    transaction_views,
    token_views,
)

urlpatterns = [
    # User
    path("user/", user_views.UserAPI.as_view(), name="user-api"),
    path(
        "reset-password/",
        user_views.ResetPasswordAPI.as_view(),
        name="reset-password-api",
    ),
    # Account
    path("accounts/", account_views.AccountAPI.as_view(), name="account-api"),
    # Category
    path("categories/", category_views.CategoryAPI.as_view(), name="categories-api"),
    # Transaction
    path(
        "transactions/",
        transaction_views.TransactionAPI.as_view(),
        name="transactions-api",
    ),
    path("token/", token_views.BearerTokenAPI.as_view(), name="token-api"),
]
