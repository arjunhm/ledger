from rest_framework import serializers
from transaction.models import Transaction

from user.serializers import UserSerializer
from account.serializers import AccountSerializer
from category.serializers import CategorySerializer


class TransactionSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # account = AccountSerializer()
    # category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = "__all__"
