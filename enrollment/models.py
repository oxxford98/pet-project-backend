from django.db import models

from canine.models import Canine
from plan.models import Plan


class Enrollment(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    canine = models.ForeignKey(Canine, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "enrollments"
