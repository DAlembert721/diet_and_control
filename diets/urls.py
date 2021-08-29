from django.urls import path

from diets.views import create_treatment, treatment_detail

urlpatterns = [
    path('doctors/<int:doctor_id>/patients/<int:patient_id>/treatments/', create_treatment, name='create_treatment'),
    path('treatments/<int:treatment_id>/', treatment_detail, name='treatment_detail'),
]