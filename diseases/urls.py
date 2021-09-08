from django.urls import path

from diseases.views import illnesses_list, patient_illnesses_assigment, list_illnesses_by_patient, \
    create_patient_familiar_illnesses, delete_patient_familiar_illnesses, list_familiar_illnesses_by_patient

urlpatterns = [
    path('illnesess/', illnesses_list, name='illnesses_list'),
    path('patients/<int:patient_id>/illnesses/<int:illness_id>/',
         patient_illnesses_assigment, name='patient_illnesses_assigment'),
    path('patients/<int:patient_id>/illnesses/',
         list_illnesses_by_patient, name='list_illnesses_by_patient'),
    path('patients/<int:patient_id>/illness/<int:illness_id>/familiar_illness/',
         create_patient_familiar_illnesses, name='create_patient_familiar_illnesses'),
    path('familiar_illness/<int:familiar_illness_id>/',
         delete_patient_familiar_illnesses, name='delete_patient_familiar_illnesses'),
    path('patients/<int:patient_id>/familiar_illness',
         list_familiar_illnesses_by_patient, name='list_familiar_illnesses_by_patient'),

]