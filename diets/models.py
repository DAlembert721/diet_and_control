from datetime import timedelta

from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import date

from accounts.models import Patient, Doctor


class Treatment(models.Model):
    description = models.CharField(max_length=250, null=False)
    progress = models.BooleanField(default=True)
    carbohydrate = models.FloatField(null=False)
    fat = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    active = models.BooleanField(default=True, null=False)
    start_date = models.DateField(null=False, auto_now=True)
    end_date = models.DateField(null=False, auto_now_add=30)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.description + ' ' + str(self.patient) + ' ' + str(self.doctor)

    class Meta:
        db_table = 'treatments'


class Menu(models.Model):
    description = models.CharField(max_length=500)
    date = models.DateField(null=False)
    active = models.BooleanField(default=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)

    def __str__(self):
        return 'Menu' + str(self.date) + ' ' + str(self.treatment_id)

    class Meta:
        db_table = 'menus'


class Schedule(models.Model):
    name = models.CharField(max_length=250, null=False)
    hour = models.TimeField(null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'schedules'


class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    carbohydrate = models.FloatField(null=False)
    fat = models.FloatField(null=False)
    protein = models.FloatField(null=False)
    recipe = models.TextField(null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True)
    menus = models.ManyToManyField(Menu, related_name='meals')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'meals'
