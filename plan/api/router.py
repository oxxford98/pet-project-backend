from django.urls import path
from rest_framework.routers import DefaultRouter
from plan.api.views import PlanApiViewSet


router_plan = DefaultRouter()
router_plan.register(prefix='', basename='plans', viewset=PlanApiViewSet)