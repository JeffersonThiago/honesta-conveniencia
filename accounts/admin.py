from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import Profile  

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_superuser"
    )
    list_display_links = ("id", "email")
    search_fields = ("first_name", "last_name", "email")
    list_per_page = 25
    ordering = ("id",)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("id", "user")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_per_page = 25
    ordering = ("id",)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(get_user_model(), UserAdmin)