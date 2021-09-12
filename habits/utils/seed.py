from habits.models import HarmfulHabit, PhysicalActivity


def create_data_physical_activity(apps, schema_editor):
    activities = [{'name': 'Poco o ningún ejercicio', 'description': 'Caso preocupante'},
                  {'name': 'Ejercicio ligero', 'description': '1-3 días a la semana'},
                  {'name': 'Ejercicio moderado', 'description': '3-5 días a la semana'},
                  {'name': 'Ejercicio fuerte', 'description': '6-7 días a la semana'},
                  {'name': 'Ejercicio muy fuerte', 'description': 'dos veces al día, entrenamientos muy duros'}]
    for activity in activities:
        PhysicalActivity(name=activity['name'], description=activity['description']).save()


def create_data_harmful_habit(apps, schema_editor):
    habits = [{'name': 'Tabaco', 'description': 'Producto agrícola procesado a partir de las hojas de Nicotiana tabacum.'},
              {'name': 'Alcohol', 'description': 'Líquido incoloro, de olor característico, soluble tanto en agua como en grasas.'},
              {'name': 'Drogas', 'description': 'Sustancias químicas que modifican el funcionamiento de nuestro cuerpo.'}]
    for habit in habits:
        HarmfulHabit(name=habit['name'], description=habit['description']).save()
