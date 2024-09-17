from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib import auth
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()

        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                raise ValidationError({'email': 'A user with this email already exists.'})
            raise ValidationError({'detail': 'An unexpected error has occurred. Please try again.'})
        except Exception:
            raise ValidationError({'detail': 'An unexpected error has occurred. Please try again.'})


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again!')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin!')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified!')

        return {
            'id': user.id,
            'email': user.email,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
