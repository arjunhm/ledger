from django.urls import path

from user.views import LoginAPI, LogoutAPI, RegisterAPI

app_name = "users"

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", LogoutAPI.as_view(), name="logout"),
]
