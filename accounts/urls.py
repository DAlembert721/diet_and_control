from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import register, user_detail, create_profiles

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('profiles/<int:user_id>/', create_profiles, name='create_profiles'),
]