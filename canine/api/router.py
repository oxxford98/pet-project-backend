from django.urls import path
from rest_framework.routers import DefaultRouter
from canine.api.views import CanineApiViewSet


router_canine = DefaultRouter()
router_canine.register(prefix='', basename='canines', viewset=CanineApiViewSet)