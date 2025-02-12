from rest_framework import generics
from rest_framework.pagination import CursorPagination

from accounts.models import Profile
from accounts.serializers import ProfileSerializer

class ListCreateProfileView(generics.ListCreateAPIView):

    queryset = Profile.objects.all()
    pagination_class = CursorPagination
    serializer_class = ProfileSerializer