# Create your models here.
from django.db import models
from django.http import Http404

from accounts.models import Patient, Doctor
from diseases.models import Illness


class Treatment(models.Model):
    # description = models.CharField(max_length=250, null=False)
    # treatment_number = models.IntegerField(null=False, unique=True)
    # carbohydrate = models.FloatField(null=False)
    # fat = models.FloatField(null=False)
    # protein = models.FloatField(null=False)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'treatments'


class BaseTreatment(models.Model):
    years_old = models.CharField(max_length=4, null=False)
    genre = models.BooleanField(null=False)
    bmi = models.FloatField(null=False)
    tmb = models.FloatField(null=False)
    carbohydrate = models.FloatField(null=False)
    fat = models.FloatField(null=False)
    protein = models.FloatField(null=False)
    illness = models.ForeignKey(Illness, null=True, on_delete=models.SET_NULL)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'Treatment: {self}'

    class Meta:
        db_table = 'base_treatments'


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
        BREAKFAST1 = 'BREAKFAST1'
        BREAKFAST2 = 'BREAKFAST2'
        SNACK = 'SNACK'
        LUNCH1 = 'LUNCH1'
        LUNCH2 = 'LUNCH2'
        LUNCH3 = 'LUNCH3'
        DINNER1 = 'DINNER1'
        DINNER2 = 'DINNER2'

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=False)
    menus = models.ManyToManyField(Menu, related_name='meal_schedules')
    schedule = models.CharField(max_length=50, null=False, choices=Schedule.choices)

    def __str__(self):
        return self.schedule + ' ' + f'${self.meal.name}'

    @staticmethod
    def update_meal_schedule(treatment_id, changes: dict):
        for schedule, meal in changes.items():
            try:
                meal_schedule = MealSchedule.objects.get(id=schedule)
            except MealSchedule.DoesNotExist:
                raise Http404
            try:
                meal_schedule.meal = Meal.objects.get(id=meal)
                meal_schedule.save()
            except Meal.DoesNotExist:
                raise Http404
        return Treatment.objects.get(id=treatment_id)

    class Meta:
        db_table = 'meal_schedules'
