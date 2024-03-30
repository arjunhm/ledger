from rest_framework import serializers

from transaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # account = AccountSerializer()
    # category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = "__all__"
