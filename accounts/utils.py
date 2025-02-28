from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


def get_access_and_refresh_token_for_user(user: User) -> dict:

    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
