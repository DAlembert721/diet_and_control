from rest_framework import serializers

from accounts.models import Patient, Doctor
from diets.models import Treatment, Menu, Meal, PersonalTreatment, MealSchedule
from diets.utils.generator import personal_treatment_generator


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'name', 'carbohydrate_kcal', 'fat_kcal',
                  'protein_kcal', 'carbohydrate_grams', 'fat_grams',
                  'protein_grams', 'image_url')


class MealScheduleSerializer(serializers.ModelSerializer):
    meal_id = serializers.IntegerField(read_only=True)
    menu_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MealSchedule
        fields = ('id', 'meal_id', 'menu_id', 'schedule')


class MenuSerializer(serializers.ModelSerializer):
    treatment_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'day', 'treatment_id')


class TreatmentSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(source='menu_set', many=True, read_only=True)
    illness_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Treatment
        fields = ('id', 'treatment_number', 'carbohydrate', 'fat',
                  'protein', 'illness_id', 'menus')


class PersonalTreatmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(read_only=True)
    doctor_id = serializers.IntegerField(read_only=True)
    treatment_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        patient = Patient.objects.get(user=validated_data["patient_id"])
        doctor = Doctor.objects.get(user=validated_data["doctor_id"])
        validated_data["patient"] = patient
        validated_data["doctor"] = doctor
        personal_treatment = personal_treatment_generator(patient, doctor)
        return personal_treatment

    class Meta:
        model = PersonalTreatment
        fields = ('id', 'treatment_id', 'patient_id', 'doctor_id', 'start_date'
                                                                   'end_date', 'active')
        read_only_fields = ('start_date', 'end_date', 'active')
