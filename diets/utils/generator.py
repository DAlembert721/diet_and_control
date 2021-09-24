from django.utils.datetime_safe import date
from sklearn import tree
from diets.models import Meal, Menu, PersonalTreatment, BaseTreatment, Treatment
from diseases.models import Illness


def base_treatments_data():
    base_treatments = BaseTreatment.objects.all()
    return [
        [treatment.years_old, treatment.genre, treatment.bmi, treatment.tmb, treatment.protein, treatment.carbohydrate,
         treatment.fat, treatment.illness.id] for treatment in base_treatments]


def treatments_data():
    treatments = Treatment.objects.all()
    return [treatment.id for treatment in treatments]


def personal_treatment_generator(patient, doctor, protein, carbohydrate, fat):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(base_treatments_data(), treatments_data())
    year_old = (date.today() - patient.birth_date).days / 365
    illnesses = Illness.objects.filter(patients__user=patient.user)
    data = [year_old, patient.sex, patient.imc, patient.tmb, protein, carbohydrate, fat, illnesses[0].id]
    prediction = clf.predict([data])
    return PersonalTreatment.objects.create(patient=patient, doctor=doctor,
                                            treatment_id=prediction[0])
