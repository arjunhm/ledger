from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class TransactionAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_object(self, id):
        try:
            return Transaction.objects.get(id=id, user=self.request.user)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        if id:
            transactions = Transaction.objects.filter(id=id, user=request.user)
        else:
            transactions = Transaction.objects.filter(user=request.user)

        per_page = request.GET.get("per_page", 10)
        page = request.GET.get("page", 1)
        paginator = Paginator(transactions, per_page)
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
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        id = request.GET.get("id") or request.data.get("id")
        transaction = self.get_object(id)
        serializer = self.serializer_class(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = request.data.get("id")
        transaction = self.get_object(id)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
