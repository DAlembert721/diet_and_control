from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from accounts.models import Patient
from diseases.models import Illness, FamiliarIllness
from diseases.serializers import IllnessSerializer, FamiliarIllnessSerializer

illnesses_response = openapi.Response('Illnesses description', IllnessSerializer(many=True))
illness_response = openapi.Response('Illness description', IllnessSerializer)

familiar_illnesses_response = openapi.Response('Familiar Illnesses description',
                                               FamiliarIllnessSerializer(many=True))
familiar_illness_response = openapi.Response('Familiar Illness description', FamiliarIllnessSerializer)


@swagger_auto_schema(method='post', request_body=IllnessSerializer,
                     responses={201: illness_response})
@swagger_auto_schema(method='get', responses={200: illnesses_response})
@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def illnesses_list(request):
    if request.method == 'POST':
        serializer = IllnessSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        illnesses = Illness.objects.all()
        serializer = IllnessSerializer(illnesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='delete')
@swagger_auto_schema(method='post', responses={200: illnesses_response})
@permission_classes([IsAuthenticated])
@api_view(['POST', 'DELETE'])
def patient_illnesses_assigment(request, patient_id, illness_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    try:
        illness = Illness.objects.get(id=illness_id)
    except Illness.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        patient.illnesses.add(illness)
        patient.save()
        illnesses = Illness.objects.filter(patients__user=patient_id)
        serializer = IllnessSerializer(illnesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        patient.illnesses.remove(illness)
        patient.save()
        return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', responses={200: illnesses_response})
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_illnesses_by_patient(request, patient_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        illnesses = Illness.objects.filter(patients__user=patient.user)
        serializer = IllnessSerializer(illnesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post',
                     request_body=FamiliarIllnessSerializer,
                     responses={201: familiar_illness_response})
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_patient_familiar_illnesses(request, patient_id, illness_id):
    try:
        Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    try:
        Illness.objects.get(id=illness_id)
    except Illness.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        serializer = FamiliarIllnessSerializer(patient_id=patient_id, illness_id=illness_id)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete')
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_patient_familiar_illnesses(request, familiar_illness_id):
    try:
        familiar_illness = FamiliarIllness.objects.get(id=familiar_illness_id)
    except FamiliarIllness.DoesNotExist:
        raise Http404

    if request.method == 'DELETE':
        familiar_illness.delete()
        return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['get'], responses={200: familiar_illnesses_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_familiar_illnesses_by_patient(request, patient_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        familiar_illnesses = FamiliarIllness.objects.filter(patient=patient)
        serializer = FamiliarIllnessSerializer(familiar_illnesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
