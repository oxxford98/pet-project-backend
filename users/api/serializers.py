from  rest_framework import serializers
from users.models import User
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'email',
            'last_login',
        ]


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_staff',
            'is_superuser',
            'is_active',
            'email',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance