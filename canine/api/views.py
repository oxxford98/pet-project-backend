from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from canine.models import Canine
from canine.api.serializers import CanineSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet


class CanineApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CanineSerializer
    queryset = Canine.objects.all()