from django.db import transaction
from django.core.cache import cache
from django.contrib.auth import authenticate
from django_filters import rest_framework as filters

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt import authentication
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts import utils
from accounts.models import Profile, User
from accounts.filters import UserFilters
from accounts.serializers import (
    ProfileSerializer,
    GetAccessTokenSerializer,
    VerifyAccountSerializer
)
from accounts.throttle import AnonVeryLowThrottle

class ListCreateProfileView(generics.ListCreateAPIView):

    filterset_class = UserFilters
    queryset = Profile.objects.all()
    pagination_class = CursorPagination
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ["id", "first_name", "last_name", "email"]
    authentication_classes = [authentication.JWTAuthentication]
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(
                        {
                            "msg": "Usuário registrado com sucesso, verifique seu e-mail para ativar a conta",
                        },
                        status=status.HTTP_201_CREATED,
                    )
            except Exception:
                return Response(
                    {
                        "msg": "Erro ao registrar o usuário",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_authenticators(self):
        if self.request.method == "GET":
            return [authentication.JWTAuthentication()]
        return []


class GetAccessTokenView(APIView):
    serializer_class = GetAccessTokenSerializer
    throttle_classes = [AnonVeryLowThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    token = utils.get_access_and_refresh_token_for_user(user)
                    return Response(token, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Usuário desativado"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {"error": "Credenciais inválidas e/ou usuário não ativado"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(generics.GenericAPIView):
    serializer_class = VerifyAccountSerializer
    throttle_classes = [AnonVeryLowThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            email = serializer.validated_data.get("email")
            code = serializer.validated_data.get("code")

            user = User.objects.filter(email=email).first()

            if user:
                if user.verification_code_is_valid(code):
                    user.activate_user()
                    return Response(
                        {"msg": "Usuário ativo com sucesso"}, 
                        status=status.HTTP_200_OK
                    )
            
            return Response({"error": "E-mail e/ou código inválido"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)