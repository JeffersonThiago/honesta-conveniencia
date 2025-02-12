from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts import views

urlpatterns = [
    path('profile/', views.ListCreateProfileView.as_view(), name='profile'),
    path('access-token/', TokenObtainPairView.as_view(), name='access-token'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
]