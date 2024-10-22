from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from account.models import Account
from account.serializers import AccountSerializer

class AccountListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user, id):
        return get_object_or_404(Account, id=id, user=user)

    def get(self, request):
        id = request.GET.get('id')
        account = self.get_object(request.user, id)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request):
        id = request.GET.get('id')
        account = self.get_object(request.user, id)
        serializer = AccountSerializer(account, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.GET.get('id')
        account = self.get_object(request.user, id)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


