from django.contrib import auth
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def validate(self, attrs):
        username = attrs.get('username', )

        if not username.isalnum():
            raise serializers.ValidationError('Username should be only contain alphanumeric characters')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=4)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', )
        password = attrs.get('password', )

        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed({'message': 'Invalid credentials, try again!', 'type': 'error'})
        if not user.is_active:
            raise AuthenticationFailed({'message': 'Account inactive, contact admin!', 'type': 'error'})
        if not user.is_verified:
            raise AuthenticationFailed({'message': 'Email is not verified!', 'type': 'warning'})

        update_last_login(None, user)
        return user.tokens()
