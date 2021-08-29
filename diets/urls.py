from django.urls import path

from diets.views import create_treatment

urlpatterns = [
    path('doctors/<int:doctor_id>/patients/<int:patient_id>/treatments/', create_treatment, name='create_treatment')
]