from rest_framework import serializers

from diseases.models import Illness, FamiliarIllness


class IllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Illness
        fields = ('id', 'name', 'description')


class FamiliarIllnessSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(read_only=True)
    illness_id = serializers.IntegerField(read_only=True)
    illness_name = serializers.CharField(read_only=True)

    class Meta:
        model = FamiliarIllness
        fields = ('patient_id, illness_id', 'patient_full_name', 'illness_name')
