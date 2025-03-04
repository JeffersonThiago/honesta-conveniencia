import secrets

from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager,
)


class UserManager(BaseUserManager):

    def create_user(
        self, email, first_name=None, last_name=None, password=None, **extra_fields
    ):

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.verification_code = user.generate_verification_code()
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, password, first_name=None, last_name=None, **extra_fields
    ):
        extra_fields = {"is_staff": True, "is_superuser": True, "is_active": True}

        user = self.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "user"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ("id", "first_name")

    def __str__(self):
        return self.email

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def generate_verification_code(self) -> str:
        verification_code = "".join(secrets.choice("0123456789") for i in range(6))
        return verification_code

    def verification_code_is_valid(self, code: str) -> bool:
        if self.verification_code == code:
            return True
        return False

    def activate_user(self) -> bool:
        self.is_active =  True
        self.save()
        return self.is_active 

    def deactivate_user(self) -> bool:
        self.is_active = False
        self.save()
        return self.is_active


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = "profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ("user__first_name",)
