from django.shortcuts import render

# Create your views here.
from drf_yasg import openapi

from diets.serializers import TreatmentSerializer

treatments_response = openapi.Response('Treatments description', TreatmentSerializer(many=True))
treatment_response = openapi.Response('Treatment description', TreatmentSerializer)
