from attr import field
from rest_framework import serializers

from rest import models

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class AccountSerializer(serializers.ModelSerializer):
    is_authenticated = serializers.BooleanField()
    phone = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = models.User
        fields = ['is_authenticated', 'username', 'first_name', 'last_name', 'email', 'phone']
