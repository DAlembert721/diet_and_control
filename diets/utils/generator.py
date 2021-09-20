from datetime import timedelta
from random import randrange

from diets.models import Meal, Menu, PersonalTreatment


def personal_treatment_generator(patient, doctor):
    return PersonalTreatment().save()
