# Create your views here.
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Patient
from habits.models import PhysicalActivity, HarmfulHabit
from habits.serializers import PhysicalActivitySerializer, HarmfulHabitSerializer

physical_activities_response = openapi.Response('Physical Activities description',
                                                PhysicalActivitySerializer(many=True))
physical_activity_response = openapi.Response('Physical Activity description', PhysicalActivitySerializer)
harmful_habits_response = openapi.Response('Harmful Habits description',
                                           HarmfulHabitSerializer(many=True))
harmful_habit_response = openapi.Response('Harmful Habit description', HarmfulHabitSerializer)


@swagger_auto_schema(methods=['post'], request_body=PhysicalActivitySerializer,
                     responses={201: physical_activity_response})
@swagger_auto_schema(method='get', responses={200: physical_activities_response})
@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def physical_activities_list(request):
    if request.method == 'POST':
        serializer = PhysicalActivitySerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        physical_activities = PhysicalActivity.objects.all()
        serializer = PhysicalActivitySerializer(physical_activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='delete')
@swagger_auto_schema(method='post', responses={200: physical_activities_response})
@permission_classes([IsAuthenticated])
@api_view(['POST', 'DELETE'])
def patient_physical_activities_assignment(request, patient_id, physical_activity_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    try:
        physical_activity = PhysicalActivity.objects.get(id=physical_activity_id)
    except PhysicalActivity.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        patient.physical_activities.add(physical_activity)
        patient.save()
        physical_activities = PhysicalActivity.objects.filter(patients__user=patient.user)
        serializer = PhysicalActivitySerializer(physical_activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        patient.physical_activities.remove(physical_activity)
        patient.save()
        return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', responses={200: physical_activities_response})
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_physical_activities_by_patient(request, patient_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        physical_activities = PhysicalActivity.objects.filter(patients__user=patient.user)
        serializer = PhysicalActivitySerializer(physical_activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'], request_body=HarmfulHabitSerializer,
                     responses={201: harmful_habit_response})
@swagger_auto_schema(method='get', responses={200: harmful_habits_response})
@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def harmful_habits_list(request):
    if request.method == 'POST':
        serializer = HarmfulHabitSerializer(request.data)
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        harmful_habits = HarmfulHabit.objects.all()
        serializer = HarmfulHabitSerializer(harmful_habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='delete')
@swagger_auto_schema(method='post', responses={200: harmful_habits_response})
@permission_classes([IsAuthenticated])
@api_view(['POST', 'DELETE'])
def patient_harmful_habits_assigment(request, patient_id, harmful_habit_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    try:
        harmful_habit = HarmfulHabit.objects.get(id=harmful_habit_id)
    except HarmfulHabit.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        patient.harmful_habits.add(harmful_habit)
        patient.save()
        harmful_habits = HarmfulHabit.objects.filter(patients__user=patient.user)
        serializer = HarmfulHabitSerializer(harmful_habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        patient.harmful_habits.remove(harmful_habit)
        patient.save()
        return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', responses={200: harmful_habits_response})
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_harmful_habits_by_patient(request, patient_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        harmful_habits = HarmfulHabit.objects.filter(patients__user=patient.user)
        serializer = HarmfulHabitSerializer(harmful_habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)