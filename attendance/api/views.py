from attendance.api.serializers import AttendanceSerializer
from attendance.models import Attendance
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class AttendanceApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()