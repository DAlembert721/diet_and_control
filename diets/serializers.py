from django.http import Http404
from rest_framework import serializers

from accounts.models import Patient, Doctor
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
    meal_schedules = MealScheduleSerializer(source='meal_schedule_set', read_only=True, many=True)

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
        fields = ('id', 'menus',
                  'protein', 'carbohydrate', 'fat')


class PersonalTreatmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(read_only=True)
    doctor_id = serializers.IntegerField(read_only=True)
    treatment = TreatmentSerializer()
    menus = serializers.ListField(write_only=True, allow_empty=True,
                                  max_length=7,
                                  child=serializers.ListSerializer(child=serializers.IntegerField()))
    selected_treatment = serializers.IntegerField(default=0, write_only=True)

    def create(self, validated_data):
        patient = Patient.objects.get(user=validated_data["patient_id"])
        doctor = Doctor.objects.get(user=validated_data["doctor_id"])
        validated_data["patient"] = patient
        validated_data["doctor"] = doctor
        if self.selected_treatment == 0:
            treatment = create_treatment(self.menus)
        else:
            try:
                treatment = Treatment.objects.get(id=self.selected_treatment)
            except Treatment.DoesNotExist:
                raise Http404
        personal_treatment = PersonalTreatment.objects.create(patient=patient, doctor=doctor, treatment=treatment)
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
