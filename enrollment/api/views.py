from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from enrollment.models import Enrollment
from enrollment.api.serializers import EnrollmentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet


class EnrollmentApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()