from rest_framework.routers import DefaultRouter

from django.urls import path

from plan.api.views import PlanApiViewSet

router_plan = DefaultRouter()
router_plan.register(prefix="", basename="plans", viewset=PlanApiViewSet)
