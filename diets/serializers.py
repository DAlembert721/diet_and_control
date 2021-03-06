from django.http import Http404
from openpyxl.cell import read_only
from rest_framework import serializers

from accounts.models import Patient, Doctor
from communications.models import Chat
from diets.models import Treatment, Menu, Meal, PersonalTreatment, MealSchedule, PersonalTreatmentTrace
from diets.utils.generator import create_treatment


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'name', 'carbohydrate_kcal', 'fat_kcal',
                  'protein_kcal', 'carbohydrate_grams', 'fat_grams',
                  'protein_grams', 'image_url')


class MealScheduleSerializer(serializers.ModelSerializer):
    menu_id = serializers.IntegerField(read_only=True)
    meal = MealSerializer(read_only=True)

    class Meta:
        model = MealSchedule
        fields = ('id', 'meal', 'menu_id', 'schedule')


class MenuSerializer(serializers.ModelSerializer):
    treatment_id = serializers.IntegerField(read_only=True)
    meal_schedules = MealScheduleSerializer(read_only=True, many=True)

    @staticmethod
    def meals(self):
        return self.meal_chedules

    class Meta:
        model = Menu
        fields = ('id', 'day', 'treatment_id', 'meal_schedules')


class TreatmentSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(source='menu_set', many=True, read_only=True)

    class Meta:
        model = Treatment
        fields = ('id', 'menus')


class GenerateTreatmentSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(source='menu_set', many=True, read_only=True)
    protein = serializers.FloatField(write_only=True)
    carbohydrate = serializers.FloatField(write_only=True)
    fat = serializers.FloatField(write_only=True)

    class Meta:
        model = Treatment
        fields = ('id', 'menus', 'protein', 'carbohydrate', 'fat')


class PersonalTreatmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(read_only=True)
    doctor_id = serializers.IntegerField(read_only=True)
    treatment = TreatmentSerializer(read_only=True, allow_null=True, required=False)
    menus = serializers.ListField(write_only=True, allow_empty=True,
                                  max_length=7,
                                  child=serializers.ListSerializer(child=serializers.IntegerField()))
    selected_treatment = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        patient = Patient.objects.get(user=validated_data["patient_id"])
        doctor = Doctor.objects.get(user=validated_data["doctor_id"])
        validated_data["patient"] = patient
        validated_data["doctor"] = doctor
        selected_treatment = validated_data.get("selected_treatment", 0)
        menus = validated_data.get("menus", [])
        if selected_treatment == 0:
            treatment = create_treatment(menus)
        else:
            try:
                treatment = Treatment.objects.get(id=selected_treatment)
            except Treatment.DoesNotExist:
                raise Http404
        personal_treatment = PersonalTreatment.objects.create(patient=patient, doctor=doctor, treatment=treatment)
        Chat.objects.get_or_create(sender=doctor, receiver=patient)
        PersonalTreatmentTrace.create_trace(personal_treatment=personal_treatment)
        return personal_treatment

    class Meta:
        model = PersonalTreatment
        fields = ('id', 'treatment', 'patient_id', 'doctor_id', 'start_date',
                  'end_date', 'active', 'menus', 'selected_treatment')
        read_only_fields = ('start_date', 'end_date', 'active', 'treatment')


class TreatmentUpdateSerializer(TreatmentSerializer):
    changes = serializers.DictField(write_only=True,
                                    child=serializers.IntegerField(allow_null=False),
                                    allow_empty=False,
                                    required=True)

    def update(self, instance, validated_data):
        treatment = MealSchedule.update_meal_schedule(treatment_id=instance.id,
                                                      changes=validated_data["changes"])
        return treatment

    class Meta:
        model = Treatment
        fields = TreatmentSerializer.Meta.fields + ('changes',)


class PersonalTreatmentTraceSerializer(serializers.ModelSerializer):
    personal_treatment_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PersonalTreatmentTrace
        fields = ('id', 'day', 'success', 'personal_treatment_id')


class UpdatePersonalTreatmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(read_only=True)
    doctor_id = serializers.IntegerField(read_only=True)
    treatment = TreatmentSerializer(read_only=True, allow_null=True, required=False)
    menus = serializers.ListField(write_only=True, max_length=7, required=True,
                                  child=serializers.ListSerializer(child=serializers.IntegerField()))

    def update(self, instance, validated_data):
        treatment = create_treatment(validated_data["menus"])
        instance.treatment = treatment
        instance.save()
        return instance

    class Meta:
        model = PersonalTreatment
        fields = ('id', 'treatment', 'patient_id', 'doctor_id', 'start_date',
                  'end_date', 'active', 'menus')
        read_only_fields = ('start_date', 'end_date', 'active', 'treatment')
