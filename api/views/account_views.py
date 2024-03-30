from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

from account.models import Account
from account.serializers import AccountSerializer


class AccountAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")

        if id:
            accounts = Account.objects.filter(id=id, user=request.user)
        else:
            accounts = Account.objects.filter(user=request.user)

        per_page = request.GET.get("per_page", 10)
        page = request.GET.get("page", 1)
        paginator = Paginator(accounts, per_page)
        page_obj = paginator.get_page(page)

        serializer = self.serializer_class(page_obj.object_list, many=True)
        return Response(
            {
                "data": serializer.data,
                "pagination": {"total_pages": paginator.num_pages, "page": page},
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("-----------", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        id = request.data.get("id")
        try:
            account = Account.objects.get(id=id, user=request.user)
        except Account.DoesNotExist:
            return Response(
                {"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(account, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print("-----------", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = request.data.get("id")
        try:
            account = Account.objects.get(id=id, user=request.user)
        except Account.DoesNotExist:
            return Response(
                {"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND
            )

        account.delete()
        return Response(
            {"message": "Account deleted"}, status=status.HTTP_204_NO_CONTENT
        )
