from django.urls import path

from category.views import (
    CategoryDetailAPI,
    CategoryListAPI,
    SubCategoryDetailAPI,
    SubCategoryListAPI,
)

urlpatterns = [
    path("list/", CategoryListAPI.as_view(), name="category-list"),
    path("detail/", CategoryDetailAPI.as_view(), name="category-detail"),
    path("subcategory/list/", SubCategoryListAPI.as_view(), name="subcategory-list"),
    path(
        "subcategory/detail/", SubCategoryDetailAPI.as_view(), name="subcategory-detail"
    ),
]
