from diets.models import Meal
from django.utils.datetime_safe import time
import pandas as pd
import numpy as np



# def create_meals_data(apps, schema_editor):
#     df = pd.read_excel("diets/utils/meals.xlsx", "preparaciones")
#     meals = []
#     for row in range(475):
#         data = np.array(df.loc[row])
#         meals.append(data)
#
#     for meal in meals:
#         Meal(name=meal[0], description=meal[10],
#              carbohydrate=meal[6], fat=meal[4],
#              protein=meal[2], recipe=meal[11],
#              schedule=schedule).save()
