from django.db import models

from users.models import User


class Canine(models.Model):
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    size = models.IntegerField()  # 1: Small, 2: Medium, 3: Large
    birth_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "canines"
