from django.db import models

# Create your models here.
from accounts.models import Patient


class Illness(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    patients = models.ManyToManyField(Patient, related_name='illnesses')

    def __str__(self):
        return 'Illness: ' + self.name

    class Meta:
        db_table = 'illnesses'


class FamiliarIllness(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    illness = models.ForeignKey(Illness, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'familiar_illnesses'
