from django.urls import path
from category.views import (
    CategoryListAPI, CategoryDetailAPI,
    SubCategoryListAPI, SubCategoryDetailAPI
)

urlpatterns = [
    path('list/', CategoryListAPI.as_view(), name='category-list'),
    path('detail/', CategoryDetailAPI.as_view(), name='category-detail'),
    path('subcategory/list/', SubCategoryListAPI.as_view(), name='subcategory-list'),
    path('subcategory/detail/', SubCategoryDetailAPI.as_view(), name='subcategory-detail'),
]
