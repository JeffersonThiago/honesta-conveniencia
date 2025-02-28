from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts import views

urlpatterns = [
    path("accounts/", 
        views.ListCreateProfileView.as_view(), 
        name="profile"
    ),
    path(
        "accounts/access-token/",
        views.GetAccessTokenView.as_view(),
        name="access-token",
    ),
    path("accounts/refresh-token/", 
        TokenRefreshView.as_view(), 
        name="refresh-token"
    ),
    path(
        "accounts/activate/", 
        views.ActivateAccountView.as_view(), 
        name="verify-account"
    ),
]
