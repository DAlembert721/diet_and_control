from diseases.models import Illness


def create_data_illness(apps, schema_editor):
    illnesses = [{'name': 'Obesidad', 'description': 'Enfermedad que consiste en tener una  cantidad excesiva de grasa corporal.'},
               {'name': 'Diabetes', 'description': 'Enfermedad en la que los niveles de glucosa (azúcar) de la sangre están muy altos.'},
               {'name': 'Hipertensión', 'description': 'Afección en la que la presión de la sangre hacia las paredes de la arteria es demasiado alta.'}]
    for illness in illnesses:
        Illness(name=illness['name'], description=illness['description']).save()
