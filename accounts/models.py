from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self, email, first_name=None, last_name=None , password=None, **extra_fields):
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None, last_name=None, **extra_fields):

        user = self.create_user(email, first_name=first_name, last_name=last_name, **extra_fields)
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    first_name = models.CharField(max_length=50, blank=True, null=False)
    last_name = models.CharField(max_length=150, blank=True, null=False)
    email = models.EmailField(unique=True, blank=True, null=False, validators=[EmailValidator()])
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "user"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ("id", "first_name")

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    
    class Meta:
        db_table = "profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ("user__first_name",)
        
