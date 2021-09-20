from django.urls import path

from diets.views import treatment_detail, create_personal_treatment

urlpatterns = [
    path('doctors/<int:doctor_id>/patients/<int:patient_id>/personal_treatments/',
         create_personal_treatment, name='create_treatment'),
    path('treatments/<int:treatment_id>/', treatment_detail, name='treatment_detail'),
]
