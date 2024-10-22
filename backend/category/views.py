from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import Category, SubCategory
from category.serializers import CategorySerializer, SubCategorySerializer


class CategoryListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        return get_object_or_404(Category, id=id)

    def get(self, request):
        id = request.GET.get("id")
        category = self.get_object(id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request):
        id = request.GET.get("id")
        category = self.get_object(id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.GET.get("id")
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoryListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category_id = request.GET.get("category_id")
        subcategories = SubCategory.objects.filter(category_id=category_id)
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)

    def post(self, request):
        category_id = request.GET.get("category_id")
        # Add category_id to the request data
        data = request.data.copy()
        data["category"] = category_id

        serializer = SubCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, category_id, id):
        return get_object_or_404(SubCategory, category_id=category_id, id=id)

    def get(self, request):
        category_id = request.GET.get("category_id")
        id = request.GET.get("id")
        subcategory = self.get_object(category_id, id)
        serializer = SubCategorySerializer(subcategory)
        return Response(serializer.data)

    def put(self, request):
        category_id = request.GET.get("category_id")
        id = request.GET.get("id")
        subcategory = self.get_object(category_id, id)

        data = request.data.copy()
        data["category"] = category_id

        serializer = SubCategorySerializer(subcategory, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        category_id = request.GET.get("category_id")
        id = request.GET.get("id")
        subcategory = self.get_object(category_id, id)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
