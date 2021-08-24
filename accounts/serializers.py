from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_password(value: str) -> str:
        return make_password(value)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }