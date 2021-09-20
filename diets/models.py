# Create your models here.
from django.db import models

from accounts.models import Patient, Doctor
from diseases.models import Illness


class Treatment(models.Model):
    description = models.CharField(max_length=250, null=False)
    treatment_number = models.IntegerField(null=False)
    carbohydrate = models.FloatField(null=False)
    fat = models.FloatField(null=False)
    protein = models.FloatField(null=False)
    illness = models.ForeignKey(Illness, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'treatments'


class PersonalTreatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, null=False)
    start_date = models.DateField(auto_now_add=1)
    end_date = models.DateField(auto_now_add=15)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Treatment of patient' + self.patient.first_name + ' ' + self.patient.last_name

    class Meta:
        db_table = 'personal_treatments'


class PersonalTreatmentTrace(models.Model):
    day = models.SmallIntegerField(null=False)
    success = models.BooleanField(null=False, default=False)
    personal_treatment = models.ForeignKey(PersonalTreatment, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return 'PersonalTreatmentTrace ' + f'${self.personal_treatment.patient.first_name} ${self.personal_treatment.patient.last_name}-${self.day}-${self.success}'

    class Meta:
        db_table = 'personal_treatment_traces'


class Menu(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    day = models.SmallIntegerField(null=False)

    def __str__(self):
        return 'Menu' + str(self.day) + ' ' + str(self.treatment_id)

    class Meta:
        db_table = 'menus'


class Meal(models.Model):
    name = models.CharField(max_length=250)
    carbohydrate_kcal = models.FloatField(null=False)
    fat_kcal = models.FloatField(null=False)
    protein_kcal = models.FloatField(null=False)
    carbohydrate_grams = models.FloatField(null=False)
    fat_grams = models.FloatField(null=False)
    protein_grams = models.FloatField(null=False)
    image_url = models.URLField(null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'meals'


class MealSchedule(models.Model):
    class Schedule(models.TextChoices):
        BREAKFAST = 'BREAKFAST'
        REFRESHMENT = 'REFRESHMENT'
        LUNCH = 'LUNCH'
        DINNER = 'DINNER'

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False)
    schedule = models.CharField(max_length=50, null=False, choices=Schedule.choices)

    def __str__(self):
        return self.schedule + ' ' + f'${self.meal.name} ${self.menu.day}'

    class Meta:
        db_table = 'meal_schedules'
