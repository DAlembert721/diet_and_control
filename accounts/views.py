from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User, Profile, Patient, PatientLog, Doctor
from accounts.serializers import UserSerializer, ProfileSerializer, DoctorSerializer, PatientSerializer, \
    PatientLogSerializer

users_response = openapi.Response('Users description', UserSerializer(many=True))
user_response = openapi.Response('User description', UserSerializer)
profiles_response = openapi.Response('Profiles description', ProfileSerializer(many=True))
profile_response = openapi.Response('Profile description', ProfileSerializer)
doctors_response = openapi.Response('Doctors description', DoctorSerializer(many=True))
doctor_response = openapi.Response('Doctor description', DoctorSerializer)
patients_response = openapi.Response('Patients description', PatientSerializer(many=True))
patient_response = openapi.Response('Patient description', PatientSerializer)
patient_logs_response = openapi.Response('Patient logs description', PatientLogSerializer(many=True))


@swagger_auto_schema(methods=['post'],
                     operation_description='Create a new User',
                     request_body=UserSerializer)
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get',
                     operation_description='Get user by user id',
                     responses={200: user_response})
@swagger_auto_schema(methods=['put'],
                     operation_description='Update user by user id',
                     request_body=UserSerializer)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get',
                     operation_description='Get all available profiles',
                     responses={200: profiles_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profiles_list(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'],
                     operation_description='Create profile of a user',
                     request_body=ProfileSerializer,
                     responses={201: profile_response})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profiles(request, user_id):
    try:
        User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get',
                     operation_description='Get profile by user id',
                     responses={302: profile_response})
@swagger_auto_schema(method='patch',
                     operation_description='Update profile by user_id',
                     request_body=ProfileSerializer, responses={200: profiles_response})
@swagger_auto_schema(method='delete',
                     operation_description='Delete profile by user_id')
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile_detail(request, profile_id):
    try:
        profile = Profile.objects.get(user_id=profile_id)
    except Profile.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    elif request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='patch',
                     operation_description='Update patient profile',
                     request_body=PatientSerializer, responses={200: patient_response})
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patient_detail(request, patient_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404

    if request.method == 'PATCH':
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get',
                     operation_description='Update history of a patient',
                     responses={200: patient_logs_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_logs_list(request, patient_id):
    try:
        patient = Patient.objects.get(user=patient_id)
    except Patient.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        logs = PatientLog.objects.filter(patient=patient)
        serializer = PatientLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get',
                     operation_description='Get all patients of a doctor using doctor_id',
                     responses={200: patients_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_patients_by_doctor(request, doctor_id):
    try:
        doctor = Doctor.objects.get(user=doctor_id)
    except Doctor.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        patients = Patient.objects.filter(personaltreatment__doctor=doctor)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
