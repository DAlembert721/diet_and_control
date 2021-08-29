from rest_framework import serializers

from accounts.models import Patient, Doctor
from diets.models import Treatment, Menu, Schedule, Meal
from diets.utils.generator import menus_generator


class MealSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'description', 'carbohydrate',
                  'fat', 'protein', 'recipe', 'schedule_id')


class MenuSerializer(serializers.ModelSerializer):
    treatment_id = serializers.IntegerField(read_only=True)
    meals = MealSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'description', 'date', 'treatment_id', 'active', 'meals')


class TreatmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(read_only=True)
    doctor_id = serializers.IntegerField(read_only=True)
    menus = MenuSerializer(source='menu_set', many=True, read_only=True)

    def create(self, validated_data):
        patient = Patient.objects.get(user=validated_data["patient_id"])
        doctor = Doctor.objects.get(user=validated_data["doctor_id"])
        validated_data["patient"] = patient
        validated_data["doctor"] = doctor
        treatment = Treatment.objects.create(**validated_data)
        menus_generator(treatment)
        treatment = Treatment.objects.get(id=treatment.id)
        return treatment

    class Meta:
        model = Treatment
        fields = ('id', 'progress', 'carbohydrate', 'fat',
                  'protein', 'active', 'start_date', 'end_date',
                  'patient_id', 'doctor_id', 'menus')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'name', 'hour')



