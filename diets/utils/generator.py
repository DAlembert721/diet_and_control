from django.http import Http404
from django.utils.datetime_safe import date
from sklearn import tree
from diets.models import Meal, Menu, PersonalTreatment, BaseTreatment, Treatment, MealSchedule
from diseases.models import Illness


def base_treatments_data():
    base_treatments = BaseTreatment.objects.all()
    return [
        [treatment.years_old, treatment.genre, treatment.bmi, treatment.tmb, treatment.protein, treatment.carbohydrate,
         treatment.fat, treatment.illness.id] for treatment in base_treatments]


def treatments_data():
    treatments = Treatment.objects.all()
    return [treatment.id for treatment in treatments]


def treatment_generator(patient, protein, carbohydrate, fat):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(base_treatments_data(), treatments_data())
    year_old = (date.today() - patient.birth_date).days / 365
    illnesses = Illness.objects.filter(patients__user=patient.user)
    data = [year_old, patient.sex, patient.imc, patient.tmb, protein, carbohydrate, fat, illnesses[0].id]
    prediction = clf.predict([data])
    return Treatment.objects.get(id=prediction)


def createTreatment(menus):
    treatment = Treatment.objects.create()
    for i, meal_schedules in dict(menus).items():
        menu = Menu.objects.create(day=i + 1, treatment=treatment)
        for meal_schedule_id in meal_schedules:
            try:
                meal_schedule = MealSchedule.objects.get(id=meal_schedule_id)
                menu.meal_schedules.add(meal_schedule)
                menu.save()
            except MealSchedule.DoesNotExist:
                raise Http404
    return Treatment.objects.get(id=treatment.id)
