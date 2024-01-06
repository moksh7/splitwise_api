from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from splitwise.models import SplitUser


class UserCreateSerializer(serializers.ModelSerializer):
    number = serializers.CharField(max_length=10, validators=[UniqueValidator(queryset=SplitUser.objects.all())])
    class Meta:
        model = SplitUser
        fields = ['number', 'name', 'email']
        