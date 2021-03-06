from django.urls import path

from diets.views import treatment_detail, create_personal_treatment, list_meals_schedules, \
    update_treatment, update_personal_treatment_trace, list_personal_treatment_traces_by_personal_treatment, \
    update_personal_treatment, treatments_generator, menu_detail, list_personal_treatments_by_patient_id

urlpatterns = [
    path('doctors/<int:doctor_id>/patients/<int:patient_id>/personal_treatments/',
         create_personal_treatment, name='create_treatment'),
    path('treatments/<int:treatment_id>/', treatment_detail, name='treatment_detail'),
    path('meals_schedule/schedule=<str:schedule>', list_meals_schedules, name='list_meals_schedules'),
    path('patients/<int:patient_id>/treatments/',
         treatments_generator, name='treatments_generator'),
    path('treatments/<int:treatment_id>/meal_schedules/', update_treatment, name='update_treatment'),
    path('personal_treatment_trace/<int:trace_id>/', update_personal_treatment_trace,
         name='update_personal_treatment_trace'),
    path('treatments/<int:treatment_id>/personal_treatment_trace/',
         list_personal_treatment_traces_by_personal_treatment,
         name='list_personal_treatment_traces_by_personal_treatment'),
    path('personal_treatments/<int:personal_treatment_id>/', update_personal_treatment,
         name='update_personal_treatment'),
    path('menus/<int:menu_id>/', menu_detail, name='menu_detail'),
    path('patients/<int:patient_id>/personal_treatments/',
         list_personal_treatments_by_patient_id, name='list_personal_treatments_by_patient_id'),
]
