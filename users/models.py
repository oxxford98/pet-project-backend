from django.contrib.auth.models import AbstractUser
from django.db import models

from role.models import Role


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    cellphone = models.CharField(max_length=20, null=True, blank=True)
    verify_code = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    identification = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    hiring_date = models.DateField(null=True, blank=True)
    second_name = models.CharField(max_length=150, null=True, blank=True)
    second_last_name = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
