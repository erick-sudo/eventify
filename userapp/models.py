from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(max_length=255, unique=True, verbose_name=("Email Address"))
    first_name=models.CharField(max_length=100, verbose_name=("First Name"))
    last_name=models.CharField(max_length=100, verbose_name=("Last Name"))
    is_active=models.BooleanField(default=True, verbose_name=("Active"))
    is_verified=models.BooleanField(default=False, verbose_name=("Verified"))
    is_staff=models.BooleanField(default=False, verbose_name=("Staff"))
    is_superuser=models.BooleanField(default=False, verbose_name=("Super User"))
    date_joined=models.DateTimeField(auto_now_add=True, verbose_name=("Date Joined"))
    last_login=models.DateTimeField(auto_now=True, verbose_name=("Last Login"))
    
    USERNAME_FIELD="email"
    
    REQUIRED_FIELDS= ["first_name", "last_name"]
    
    objects= UserManager()
    
    def __str__(self) -> str:
        return self.email
    
    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
