from django.http import Http404

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Patient, Doctor
from diets.models import Treatment, MealSchedule, Menu, PersonalTreatmentTrace, PersonalTreatment
from diets.serializers import TreatmentSerializer, PersonalTreatmentSerializer, MealScheduleSerializer, \
    GenerateTreatmentSerializer, TreatmentUpdateSerializer, PersonalTreatmentTraceSerializer, MenuSerializer, \
    UpdatePersonalTreatmentSerializer
from diets.utils.generator import treatment_generator

treatments_response = openapi.Response('Treatments description', TreatmentSerializer(many=True))
treatment_response = openapi.Response('Treatment description', TreatmentSerializer)
generate_treatment_response = openapi.Response('Generate Treatment description', GenerateTreatmentSerializer)
personal_treatment_response = openapi.Response('PersonalTreatment description', PersonalTreatmentSerializer)
personal_treatments_response = openapi.Response('List of PersonalTreatments description',
                                                PersonalTreatmentSerializer(many=True))
meal_schedules_response = openapi.Response('MealScheduleResponse description', MealScheduleSerializer(many=True))
update_treatment_response = openapi.Response('Update Treatment Response description', TreatmentUpdateSerializer)
personal_treatment_trace_response = openapi.Response('PersonalTreatmentTrace Response description',
                                                     PersonalTreatmentTraceSerializer)
personal_treatment_traces_response = openapi.Response('PersonalTreatmentTraces Response description',
                                                      PersonalTreatmentTraceSerializer(many=True))
menu_response = openapi.Response('Menu Response description', MenuSerializer)
update_personal_treatment_response = openapi.Response('Update Personal Treatment Response',
                                                      UpdatePersonalTreatmentSerializer)


@swagger_auto_schema(methods=['post'],
                     operation_description='Create personal treatment for a patient',
                     request_body=PersonalTreatmentSerializer,
                     responses={201: personal_treatment_response})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_personal_treatment(request, doctor_id, patient_id):
    try:
        Patient.objects.get(patients_id=patient_id)
    except Patient.DoesNotExist:
        raise Http404

    try:
        Doctor.objects.get(doctors_id=doctor_id)
    except Doctor.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        serializer = PersonalTreatmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient_id=patient_id, doctor_id=doctor_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['get'],
                     operation_description='Get treatment detail by treatment Id',
                     responses={302: treatment_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def treatment_detail(request, treatment_id):
    try:
        treatment = Treatment.objects.get(id=treatment_id)
    except Treatment.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


@swagger_auto_schema(methods=['get'],
                     operation_description='Get list of meals by schedule (ex: LUNCH3)',
                     responses={200: meal_schedules_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meals_schedules(request, schedule):
    if request.method == 'GET':
        if schedule is not None:
            meal_schedules = MealSchedule.objects.filter(schedule=schedule)
        else:
            meal_schedules = MealSchedule.objects.all()
        serializer = MealScheduleSerializer(meal_schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'],
                     operation_description='Generate treatment for a patient with patient_id',
                     request_body=GenerateTreatmentSerializer,
                     responses={200: treatment_response})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def treatments_generator(request, patient_id):
    try:
        patient = Patient.objects.get(patients_id=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        serializer = GenerateTreatmentSerializer(data=request.data)
        if serializer.is_valid():
            treatment = treatment_generator(patient, serializer.validated_data['protein'],
                                            serializer.validated_data['carbohydrate'], serializer.validated_data['fat'])
            return Response(GenerateTreatmentSerializer(treatment).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['put'],
                     operation_description='Update meal schedule of a treatment',
                     request_body=TreatmentUpdateSerializer,
                     responses={200: update_treatment_response})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_treatment(request, treatment_id):
    try:
        treatment = Treatment.objects.get(id=treatment_id)
    except Treatment.DoesNotExist:
        raise Http404

    if request.method == 'PUT':
        serializer = TreatmentUpdateSerializer(treatment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['put'],
                     operation_description='Update personal treatment trace to ok',
                     responses={200: personal_treatment_trace_response})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_personal_treatment_trace(request, trace_id):
    try:
        trace = PersonalTreatmentTrace.objects.get(id=trace_id)
    except PersonalTreatmentTrace.DoesNotExist:
        raise Http404

    if request.method == 'PUT':
        trace.success = True
        trace.save()
        return Response(PersonalTreatmentSerializer(trace).data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['get'],
                     operation_description='List all traces of personal treatment By personal treatment id',
                     responses={200: personal_treatment_traces_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_personal_treatment_traces_by_personal_treatment(request, treatment_id):
    try:
        personal_treatment = PersonalTreatment.objects.get(id=treatment_id)
    except Treatment.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        traces = PersonalTreatmentTrace.objects.filter(personal_treatment=personal_treatment)
        serializer = PersonalTreatmentTraceSerializer(traces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['get'],
                     operation_description='Get menu detail by id',
                     responses={200: menu_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def menu_detail(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


@swagger_auto_schema(methods=['get'],
                     operation_description='Get all personal treatments of a patient',
                     responses={200: personal_treatments_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_personal_treatments_by_patient_id(request, patient_id):
    try:
        patient = Patient.objects.get(patients_id=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        personal_treatments = PersonalTreatment.objects.filter(patient=patient)
        serializer = PersonalTreatmentSerializer(personal_treatments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['put'],
                     operation_description='Update personal treatment by id',
                     request_body=UpdatePersonalTreatmentSerializer,
                     responses={200: update_personal_treatment_response})
@swagger_auto_schema(methods=['patch'],
                     operation_description='Close personal_treatment changing active flag from true to False using personal treatment id',
                     responses={200: personal_treatment_response})
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_personal_treatment(request, personal_treatment_id):
    try:
        personal_treatment = PersonalTreatment.objects.get(id=personal_treatment_id)
    except PersonalTreatment.DoesNotExist:
        raise Http404
    if request.method == 'PUT':
        serializer = UpdatePersonalTreatmentSerializer(personal_treatment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        personal_treatment.active = False
        personal_treatment.save()
        serializer = PersonalTreatmentSerializer(personal_treatment)
        return Response(serializer.data, status=status.HTTP_200_OK)
