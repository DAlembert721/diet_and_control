from rest_framework import serializers

from accounts.models import Patient
from diseases.models import Illness, FamiliarIllness


class IllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Illness
        fields = ('id', 'name', 'description')


class FamiliarIllnessSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(read_only=True)
    illness_id = serializers.IntegerField(read_only=True)
    illness_name = serializers.CharField(read_only=True)
    patient_full_name = serializers.SerializerMethodField('get_patient_full_name', read_only=True)

    @staticmethod
    def get_patient_full_name(self):
        patient = self.familiar_illness.patient
        full_name = f'{patient.first_name} {patient.last_name}'
        return full_name

    def create(self, validated_data):
        patient = Patient.objects.get(user=validated_data["patient_id"])
        validated_data["patient"] = patient
        illness = Illness.objects.get(user=validated_data["illness_id"])
        validated_data["illness"] = illness
        familiar_illness = FamiliarIllness.objects.create(**validated_data)
        return familiar_illness

    class Meta:
        model = FamiliarIllness
        fields = ('patient_id', 'illness_id', 'patient_full_name', 'illness_name')
