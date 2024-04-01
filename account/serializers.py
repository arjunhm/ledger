from rest_framework import serializers

from account.models import Account
from user.serializers import UserSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        user = UserSerializer()
