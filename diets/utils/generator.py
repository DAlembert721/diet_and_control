from datetime import timedelta
from random import randrange

from diets.models import Meal, Menu, Schedule


def meal_generator(menu, schedule_name):
    schedule = Schedule.objects.get(name=schedule_name)
    meals = list(Meal.objects.filter(schedule=schedule))
    meal = meals[randrange(len(meals))]
    menu.meals.add(meal)
    menu.save()


def menus_generator(treatment):
    for i in range(30):
        # menu = Menu(
        #     description=str(treatment.id) + '-Menu-' + str(i),
        #     date=treatment.start_date + timedelta(i),
        #     treatment=treatment).save()
        menu = Menu.objects.create(**{
            'description': str(treatment.id) + '-Menu-' + str(i),
            'date': treatment.start_date + timedelta(i),
            'treatment': treatment
        })
        meal_generator(menu, 'breakfast')
        meal_generator(menu, 'lunch')
        meal_generator(menu, 'dinner')
