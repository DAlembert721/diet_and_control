from diets.models import Meal, Schedule
from django.utils.datetime_safe import time
import pandas as pd
import numpy as np

def create_data(apps, schema_editor):
    schedules = [{'name': 'breakfast', 'date': '07:00:00'},
                 {'name': 'lunch', 'date': '13:00:00'},
                 {'name': 'dinner', 'date': '19:00:00'}]
    for schedule in schedules:
        Schedule(name=schedule['name'], hour=schedule['date']).save()


def create_meals_data(apps, schema_editor):
    df = pd.read_excel("diets/utils/meals.xlsx", "preparaciones")
    meals = []
    for row in range(475):
        data = np.array(df.loc[row])
        meals.append(data)
    
    for meal in meals:
        schedule = Schedule.objects.get(name=meal[12])
        Meal(name=meal[0], description=meal[10],
             carbohydrate=meal[6], fat=meal[4],
             protein=meal[2], recipe=meal[11],
             schedule=schedule).save()

    # meals = [{'name': 'Banana', 'description': 'fruit', 'carbohydrate': 120.0, 'fat': 150.0, 'protein': 150.0,
    #           'recipe': None, 'schedule_name': 'breakfast'},
    #          {'name': 'Papaya', 'description': 'fruit', 'carbohydrate': 120.0, 'fat': 150.0, 'protein': 150.0,
    #           'recipe': None, 'schedule_name': 'breakfast'},
    #          {'name': 'Aji de Gallina', 'description': 'Plato de aji', 'carbohydrate': 120.0, 'fat': 150.0,
    #           'protein': 150.0, 'recipe': 'recipe', 'schedule_name': 'lunch'},
    #          {'name': 'Ceviche', 'description': 'Fish dish', 'carbohydrate': 120.0, 'fat': 150.0, 'protein': 150.0,
    #           'recipe': 'recipe', 'schedule_name': 'lunch'},
    #          {'name': 'KFC', 'description': 'Description', 'carbohydrate': 120.0, 'fat': 150.0, 'protein': 150.0,
    #           'recipe': 'recipe', 'schedule_name': 'dinner'},
    #          {'name': 'Pan', 'description': 'Description', 'carbohydrate': 120.0, 'fat': 150.0, 'protein': 150.0,
    #           'recipe': None, 'schedule_name': 'dinner'}]

    # for meal in meals:
    #     schedule = Schedule.objects.get(name=meal['schedule_name'])
    #     Meal(name=meal.get('name'), description=meal.get('description'),
    #          carbohydrate=meal.get('carbohydrate'), fat=meal.get('fat'),
    #          protein=meal.get('protein'), recipe=meal.get('recipe'),
    #          schedule=schedule).save()
