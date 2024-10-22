from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate 
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer


class RegisterAPI(views.APIView):

    permission_classes = []        

    def post(self, request):
       serializer = serializers.RegisterSerializer(data=request.data)
       if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "Registered successfully"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(views.APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return Response({
                "user": UserSerializer(user).data,
                "message": "success"
            }, status=status.HTTP_200_OK)

        return Response({
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            'message': 'Logged out successfully'
        })


