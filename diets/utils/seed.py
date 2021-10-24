from diets.models import Meal, Treatment, BaseTreatment, MealSchedule, Menu
import pandas as pd
import numpy as np

from diseases.models import Illness


def create_meals_data(apps, schema_editor):
    df = pd.read_excel("diets/utils/meals_v2.xlsx", "meals")
    meals = []
    for row in range(259):
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
    if genre == 'Masculino':
        return True
    elif genre == 'Femenino':
        return False


def define_illness(illness):
    if illness == 'OBESIDAD':
        return 1
    elif illness == 'DIABETES':
        return 50
    elif illness == 'HIPERTENSION':
        return 100


def create_treatments(apps, schema_editor):
    df = pd.read_excel("diets/utils/meals_v2.xlsx", "patients_data")
    treatments = []
    for row in range(20):
        data = np.array(df.loc[row])
        treatments.append(data)
    for treatment in treatments:
        Treatment(id=int(treatment[8])).save()


def create_base_treatments(apps, schema_editor):
    df = pd.read_excel("diets/utils/meals_v2.xlsx", "patients_data")
    rows = []
    for row in range(20):
        data = np.array(df.loc[row])
        rows.append(data)
    for row in rows:
        treatment = Treatment.objects.get(id=int(row[8]))
        illness = Illness.objects.get(id=define_illness(row[7]))
        BaseTreatment(years_old=row[0], genre=define_genre(row[1]),
                      bmi=float(row[2]), tmb=float(row[3]),
                      protein=float(row[4]), carbohydrate=float(row[5]),
                      fat=float(row[6]), illness=illness,
                      treatment=treatment).save()


def create_menus_data(apps, schema_editor):
    df = pd.read_excel("diets/utils/meals_v2.xlsx", "menus")
    menus = []
    for row in range(140):
        data = np.array(df.loc[row])
        menus.append(data)
    for menu in menus:
        Menu(
           treatment_id=menu[0],
           day=int(menu[1])
        ).save()


def create_meal_schedule(apps, schema_editor):
    df = pd.read_excel("diets/utils/meals_v2.xlsx", "menus")
    rows = []
    for row in range(140):
        data = np.array(df.loc[row])
        rows.append(data)
    for row in rows:
        menu = Menu.objects.get(treatment_id=row[0], day=row[1])
        schedule = MealSchedule.objects.create(meal_id=row[2], schedule='BREAKFAST1')
        menu.meal_schedules.add(schedule)
        menu.save()
        schedule = MealSchedule.objects.create(meal_id=row[3], schedule='BREAKFAST2')
        menu.meal_schedules.add(schedule)
        menu.save()
        schedule = MealSchedule.objects.create(meal_id=row[4], schedule='LUNCH1')
        menu.meal_schedules.add(schedule)
        menu.save()
        schedule = MealSchedule.objects.create(meal_id=row[5], schedule='LUNCH2')
        menu.meal_schedules.add(schedule)
        menu.save()
        schedule = MealSchedule.objects.create(meal_id=row[6], schedule='LUNCH3')
        menu.meal_schedules.add(schedule)
        menu.save()
        schedule = MealSchedule.objects.create(meal_id=row[7], schedule='DINNER1')
        menu.meal_schedules.add(schedule)
        menu.save()
        schedule = MealSchedule.objects.create(meal_id=row[8], schedule='DINNER2')
        menu.meal_schedules.add(schedule)
        menu.save()
        schedule = MealSchedule.objects.create(meal_id=row[9], schedule='SNACK')
        menu.meal_schedules.add(schedule)
        menu.save()
