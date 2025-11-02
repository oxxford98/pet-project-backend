from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from plan.models import Plan
from plan.api.serializers import PlanSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet


class PlanApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()