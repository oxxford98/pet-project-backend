from django.db import models
from canine.models import Canine


class Attendance(models.Model):
    canine = models.ForeignKey(Canine, on_delete=models.PROTECT)
    incoming_time = models.DateTimeField()
    outgoing_time = models.DateTimeField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    type_service_incoming = models.IntegerField() # 1: by client, 2: by school route
    type_service_outgoing = models.IntegerField(blank=True, null=True) # 1: by client, 2: by school route
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
