from diseases.models import Illness


def create_data_illness(apps, schema_editor):
    illnesses = [{'id': 1, 'name': 'OBESIDAD', 'description': 'Enfermedad que consiste en tener una  cantidad excesiva de grasa corporal.'},
               {'id': 50, 'name': 'DIABETES', 'description': 'Enfermedad en la que los niveles de glucosa (azúcar) de la sangre están muy altos.'},
               {'id': 100, 'name': 'HIPERTENSION', 'description': 'Afección en la que la presión de la sangre hacia las paredes de la arteria es demasiado alta.'}]
    for illness in illnesses:
        Illness(id=illness['id'], name=illness['name'], description=illness['description']).save()
