from django.urls import path
from views import user_views

urlpatterns = [
    # User
    path("user/", user_views.UserAPI.as_view(), name="user-api"),
    path(
        "reset-password/",
        user_views.ResetPasswordAPI.as_view(),
        name="reset-password-api",
    ),
]
