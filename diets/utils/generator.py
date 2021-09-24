from sklearn import tree

import pandas as pd

from diets.models import Meal, Menu, PersonalTreatment


clf = tree.DecisionTreeClassifier()

def personal_treatment_generator(patient, doctor):
    return PersonalTreatment().save()
