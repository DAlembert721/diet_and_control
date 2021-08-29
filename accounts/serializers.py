from django.utils.datetime_safe import date
from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from accounts.models import User, Profile, Doctor, Patient


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


class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["user_id"])
        validated_data["user"] = user
        validated_data["register_date"] = date.today()
        validated_data["type"] = validated_data["type"].lower()
        profile = None
        if validated_data["type"] == "doctor":
            profile = Doctor.objects.create(**validated_data)
        elif validated_data["type"] == "patient":
            profile = Patient.objects.create(**validated_data)
        return profile

    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'birth_date', 'phone',
                  'register_date', 'user_email', 'user_username', 'sex', 'doi')
        read_only_fields = ('register_date', 'user')


class DoctorSerializer(ProfileSerializer):
    class Meta:
        model = Doctor
        fields = ProfileSerializer.Meta.fields + ('license_number',)


class PatientSerializer(ProfileSerializer):
    class Meta:
        model = Patient
        fields = ProfileSerializer.Meta.fields + ('height', 'weight', 'arm', 'abdominal',
                                                  'hip', 'imc', 'tmb')
