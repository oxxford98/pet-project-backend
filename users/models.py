from django.db import models
from django.contrib.auth.models import AbstractUser
from role.models import Role


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    cellphone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


