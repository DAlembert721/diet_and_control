from django.utils.datetime_safe import time

from diets.models import Meal


def create_meals_data(apps, schema_editor):
    return
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
    #
    # for meal in meals:
    #     Meal(name=meal.get('name'), description=meal.get('description'),
    #          carbohydrate=meal.get('carbohydrate'), fat=meal.get('fat'),
    #          protein=meal.get('protein'), recipe=meal.get('recipe'),
    #          ).save()
