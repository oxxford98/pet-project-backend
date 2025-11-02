from django.db import models

# Create your models here.
class Role(models.Model):
    DIRECTOR = 'DIRECTOR'
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"
    TRAINER = "TRAINER"

    ROLE_CHOICES = [
        (DIRECTOR, 'Director'),
        (ADMIN, "Administrador"),
        (CLIENT, "Cliente"),
        (TRAINER, "Entrenador"),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
