from django.urls import path
from api.views import user_views, account_views


urlpatterns = [
    # User
    path("user/", user_views.UserAPI.as_view(), name="user-api"),
    path(
        "reset-password/",
        user_views.ResetPasswordAPI.as_view(),
        name="reset-password-api",
    ),
    path("accounts/", account_views.AccountAPI.as_view(), name="account-api"),
]
