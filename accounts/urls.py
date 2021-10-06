from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import register, user_detail, create_profiles, profile_detail, patient_detail, patient_logs_list, \
    list_patients_by_doctor

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('users/<int:user_id>/profiles/', create_profiles, name='create_profiles'),
    path('profiles/<int:profile_id>/', profile_detail, name='profile_detail'),
    path('patients/<int:patient_id>/', patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/logs/', patient_logs_list, name='patient_logs_list'),
    path('doctors/<int:doctor_id>/patients/', list_patients_by_doctor, name="list_patients_by_doctor"),
]
