from accounts.models import Profile
from django_filters import rest_framework as filters


class UserFilters(filters.FilterSet):
    
    email = filters.CharFilter(
        field_name="user__email",
        lookup_expr="icontains",
    )
    first_name = filters.CharFilter(
        field_name="user__first_name",
        lookup_expr="icontains",
    )
    last_name = filters.CharFilter(
        field_name="user__last_name",
        lookup_expr="icontains",
    )
    is_active = filters.BooleanFilter(
        field_name="user__is_active"
    )
    class Meta:
        
        model = Profile
        fields = [
            "email",
            "first_name",
            "last_name",
            "is_active"
        ]
