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
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'profiles'


class Doctor(models.Model):
    doctors = models.OneToOneField(Profile, auto_created=True, on_delete=models.CASCADE,
                                   primary_key=True, serialize=False)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return self.license_number

    class Meta:
        db_table = 'doctors'


class Patient(models.Model):
    patients = models.OneToOneField(Profile, auto_created=True, on_delete=models.CASCADE,
                                    primary_key=True, serialize=False)
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
