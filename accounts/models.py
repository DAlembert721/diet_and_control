from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField('active', default=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email + '-' + self.username

    class Meta:
        db_table = 'users'


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, serialize=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, null=True)
    birth_date = models.DateField()
    sex = models.BooleanField()
    phone = models.CharField(max_length=12)
    doi = models.CharField(max_length=15)
    type = models.CharField(max_length=60, null=True)
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'profiles'


class Doctor(Profile):
    doctors = models.OneToOneField(Profile, auto_created=True, on_delete=models.CASCADE, primary_key=True,
                                   serialize=False, parent_link=True)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return self.license_number

    class Meta:
        db_table = 'doctors'


class Patient(Profile):
    patients = models.OneToOneField(Profile, auto_created=True, on_delete=models.CASCADE, primary_key=True,
                                    serialize=False, parent_link=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    arm = models.FloatField(null=True)
    abdominal = models.FloatField(null=True)
    hip = models.FloatField(null=True)
    imc = models.FloatField(null=True)
    tmb = models.FloatField(null=True)

    def __str__(self):
        return self.patients.doi

    class Meta:
        db_table = 'patients'


class PatientLog(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    height = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    arm = models.FloatField(null=False)
    abdominal = models.FloatField(null=False)
    hip = models.FloatField(null=False)
    imc = models.FloatField(null=False)
    tmb = models.FloatField(null=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient.doi

    class Meta:
        db_table = 'patient_logs'


class PrivacyTermsAccept(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    accept = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.profile.first_name + ' ' + self.profile.last_name + ':OK'

    class Meta:
        db_table = 'privacy_terms_accept'
