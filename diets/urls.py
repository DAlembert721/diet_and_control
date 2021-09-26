from django.urls import path

from diets.views import treatment_detail, create_personal_treatment, list_meals_schedules, treatment_generator, \
    update_treatment

urlpatterns = [
    path('doctors/<int:doctor_id>/patients/<int:patient_id>/personal_treatments/',
         create_personal_treatment, name='create_treatment'),
    path('treatments/<int:treatment_id>/', treatment_detail, name='treatment_detail'),
    path('meals_schedule/schedule=<str:schedule>', list_meals_schedules, name='list_meals_schedules'),
    path('patients/<int:patient_id>/treatments/',
         treatment_generator, name='treatment_generator'),
    path('treatments/<int:treatment_id>/meal_schedules/', update_treatment, name='update_treatment'),
]
