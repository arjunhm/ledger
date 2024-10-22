from django.urls import path
from account import views

urlpatterns = [
    path('list/', views.AccountListAPI.as_view(), name='account-list'),
    path('detail/', views.AccountDetailAPI.as_view(), name='account-detail'),
]


