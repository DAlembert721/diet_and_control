from django.urls import path

from habits.views import physical_activities_list, patient_physical_activities_assignment, \
    list_physical_activities_by_patient, harmful_habits_list, patient_harmful_habits_assigment, \
    list_harmful_habits_by_patient

urlpatterns = [
    path('physical_activities/', physical_activities_list, name='physical_activities_list'),
    path('patients/<int:patient_id>/physical_activities/<int:physical_activity_id>/',
         patient_physical_activities_assignment, name='patient_physical_activities_assignment'),
    path('patients/<int:patient_id>/physical_activities/', list_physical_activities_by_patient,
         name='list_physical_activities_by_patient'),
    path('harmful_habits/', harmful_habits_list, name='harmful_habits__list'),
    path('patients/<int:patient_id>/harmful_habits/<int:harmful_habit_id>/',
         patient_harmful_habits_assigment, name='patient_harmful_habits_assigment'),
    path('patients/<int:patient_id>/harmful_habits/', list_harmful_habits_by_patient,
         name='list_harmful_habits_by_patient'),
]
