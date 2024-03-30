from rest_framework import serializers
from user.serializer import UserSerializer
from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        user = UserSerializer()
