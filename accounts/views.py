from django.db import transaction
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
)


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
                            "data": serializer.data,
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

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                token = self.get_access_and_refresh_token_for_user(user)
                return Response(token, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Conta não ativada. Verifique seu email."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"error": "Credenciais inválidas"},
                status=status.HTTP_401_UNAUTHORIZED,
            )



class ActivateAccountView(generics.GenericAPIView):
    serializer_class = serializers.Serializer

    def post(self, request, verification_code, email):
        pass
