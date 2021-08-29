from rest_framework import serializers

from accounts.models import Patient, Doctor
from diets.models import Treatment, Menu, Schedule, Meal
from diets.utils.generator import menus_generator


class TreatmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(source='patient.id', read_only=True)
    doctor_id = serializers.IntegerField(source='doctor.id', read_only=True)
    menus = serializers.SerializerMethodField(method_name='get_all_menus', read_only=True)

    @staticmethod
    def get_all_menus(self):
        menus = Menu.objects.filter(treatment=self)
        return MenuSerializer(menus, many=True)

    def create(self, validated_data):
        patient = Patient.objects.get(user=validated_data["patient_id"])
        doctor = Doctor.objects.get(user=validated_data["doctor_id"])
        validated_data["patient"] = patient
        validated_data["doctor"] = doctor
        treatment = Treatment.objects.create(**validated_data)
        menus_generator(treatment)
        return treatment

    class Meta:
        model = Treatment
        fields = ('id', 'progress', 'carbohydrate', 'fat',
                  'protein', 'active', 'start_date', 'end_date',
                  'patient_id', 'doctor_id', 'menus')


class MenuSerializer(serializers.ModelSerializer):
    treatment_id = serializers.IntegerField(source='treatment.id', read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'description', 'date', 'treatment_id', 'active')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'name', 'hour')


class MealSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(source='schedule.id', read_only=True)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'description', 'carbohydrate',
                  'fat', 'protein', 'recipe', 'schedule_id')
