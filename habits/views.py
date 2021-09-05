# Create your views here.
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Patient
from habits.models import PhysicalActivity
from habits.serializers import PhysicalActivitySerializer

physical_activities_response = openapi.Response('Physical Activities description',
                                                PhysicalActivitySerializer(many=True))
physical_activity_response = openapi.Response('Physical Activity description', PhysicalActivitySerializer)


@swagger_auto_schema(methods=['post'], request_body=PhysicalActivitySerializer,
                     responses={201: physical_activity_response})
@swagger_auto_schema(method='get', responses={200: physical_activities_response})
@permission_classes([IsAuthenticated])
@api_view(['POST'])
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
