from django.urls import path
from rest_framework.routers import DefaultRouter
from canine.api.views import CanineApiViewSet, get_canine_by_client


router_canine = DefaultRouter()
router_canine.register(prefix='', basename='canines', viewset=CanineApiViewSet)


urlpatterns = [
    path('canine/by-client', get_canine_by_client),
]