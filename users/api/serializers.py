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
            'cellphone',
            'role',
            'created_at',
            'address',
            'identification',
            'birth_date',
            'hiring_date',
            'second_name',
            'second_last_name',
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
            'cellphone',
            'role',
            'address',
            'identification',
            'birth_date',
            'hiring_date',
            'second_name',
            'second_last_name',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email es requerido")
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verify_code = serializers.CharField(max_length=20, required=True)
    new_password = serializers.CharField(min_length=8, required=True)
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email es requerido")
        return value.lower()
    
    def validate_verify_code(self, value):
        if not value:
            raise serializers.ValidationError("Código de verificación es requerido")
        return value.upper()
    
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return value