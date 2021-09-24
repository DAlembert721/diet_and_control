from diets.models import Meal, Treatment, BaseTreatment, MealSchedule
from django.utils.datetime_safe import time
import pandas as pd
import numpy as np

from diseases.models import Illness


def create_meals_data(apps, schema_editor):
    df = pd.read_excel("diets/utils/meals_v2.xlsx", "meals")
    meals = []
    for row in range(34):
        data = np.array(df.loc[row])
        meals.append(data)

    for meal in meals:
        Meal(
            id=meal[0],
            name=meal[1],
            carbohydrate_kcal=meal[7],
            fat_kcal=meal[6],
            protein_kcal=meal[5],
            protein_grams=meal[8],
            fat_grams=meal[9],
            carbohydrate_grams=meal[10],
            image_url=meal[11]
        ).save()


def define_genre(genre):
    if genre == 'M':
        return True
    elif genre == 'F':
        return False


def define_illness(illness):
    if illness == 'OBESIDAD':
        return 1
    elif illness == 'DIABETES':
        return 50
    elif illness == 'HIPER':
        return 100


def create_treatments(apps, schema_editor):
    df = pd.read_csv('diets/utils/TREATMENTS.csv', sep=',')
    for i in range(df.shape[0] - 1):
        treatment = Treatment.objects.get_or_create(treatment_number=int(df['PLAN'].values[i]))


def create_base_treatments(apps, schema_editor):
    df = pd.read_csv('diets/utils/TREATMENTS.csv', sep=',')
    for i in range(df.shape[0] - 1):
        treatment = Treatment.objects.get(treatment_number=int(df['PLAN'].values[i]))
        illness = Illness.objects.get(id=define_illness(df['ENFERMEDAD'].values[i]))
        BaseTreatment(years_old=df['EDAD'].values[i], genre=define_genre(df['GENERO'].values[i]),
                      bmi=float(df['BMI'].values[i]), tmb=float(df['TMB'].values[i]),
                      protein=float(df['PROT'].values[i]), carbohydrate=float(df['CARB'].values[i]),
                      fat=float(df['GRA'].values[i]), illness=illness,
                      treatment=treatment).save()
