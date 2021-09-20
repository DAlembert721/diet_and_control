from django.utils.datetime_safe import date
from rest_framework import serializers

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from accounts.models import User, Profile, Doctor, Patient, PatientLog


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
    user_email = serializers.CharField(read_only=True)
    user_username = serializers.CharField(read_only=True)

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
                  'register_date', 'user_email', 'user_username', 'sex', 'doi', 'type')
        read_only_fields = ('register_date', 'user')


class DoctorSerializer(ProfileSerializer):
    class Meta:
        model = Doctor
        fields = ProfileSerializer.Meta.fields + ('license_number',)


class PatientSerializer(ProfileSerializer):
    def update(self, instance, validated_data):
        if instance.tmb is not None:
            PatientLog(patient=instance, height=instance.height, weight=instance.weight,
                       arm=instance.arm, abdominal=instance.abdominal, hip=instance.hip,
                       imc=instance.imc, tmb=instance.tmb).save()
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.arm = validated_data.get('arm', instance.arm)
        instance.abdominal = validated_data.get('abdominal', instance.abdominal)
        instance.hip = validated_data.get('hip', instance.hip)
        instance.imc = validated_data.get('imc', instance.imc)
        instance.tmb = validated_data.get('tmb', instance.tmb)
        instance.save()
        return instance

    class Meta:
        model = Patient
        fields = ProfileSerializer.Meta.fields + ('height', 'weight', 'arm', 'abdominal',
                                                  'hip', 'imc', 'tmb')


class PatientLogSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientLog
        fields = ('id', 'patient_id', 'height', 'weight', 'arm', 'abdominal',
                  'hip', 'imc', 'tmb', 'date')
        read_only_fields = ('date',)
