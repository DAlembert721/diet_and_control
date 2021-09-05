from django.db import models


# Create your models here.
from accounts.models import Patient


class PhysicalActivity(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    patients = models.ManyToManyField(Patient, related_name='physical_activities')

    def __str__(self):
        return 'Activity: ' + self.name

    class Meta:
        db_table = 'physical_activities'


class HarmfulHabit(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    patients = models.ManyToManyField(Patient, related_name='harmful_habits')

    def __str__(self):
        return 'Harmful Habit: ' + self.name

    class Meta:
        db_table = 'harmful_habits'
