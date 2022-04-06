from rest_framework import serializers
from .models import Bond
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]


class BondSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bond
        fields = "__all__"
