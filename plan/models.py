from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_days = models.IntegerField()
    transport_type = (
        models.IntegerField()
    )  # 1: complete, 2: only morning, 3: only afternoon, 4: none
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "plans"
