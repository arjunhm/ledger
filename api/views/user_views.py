from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user.models import User
from user.serializers import UserSerializer


class UserAPI(views.APIView):
    permission_classes = []
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # TODO Confirm if self is required
        if request.user.is_authenticated:
            serializer = self.serializer_class(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN
        )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {"message": "Please logout to create an account"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            return Response(
                {"message": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(email=email, password=None)
        user.set_password(password)
        user.save()

        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.request.user.delete()
            return Response({"message": "User deleted"}, status=status.HTTP_200_OK)

        return Response(
            {"message": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN
        )


class ResetPasswordAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "An email has been sent with a link to reset the password"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        password = request.data.get("password")
        password2 = request.data.get("password2")
        if password != password2:
            return Response(
                {"message": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = self.request.user
        user.set_password(password)
        user.save()

        return Response(
            {"message": "Password has been reset"}, status=status.HTTP_200_OK
        )
