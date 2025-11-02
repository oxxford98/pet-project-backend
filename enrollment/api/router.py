from django.urls import path
from rest_framework.routers import DefaultRouter
from enrollment.api.views import EnrollmentApiViewSet


router_enrollment = DefaultRouter()
router_enrollment.register(prefix='', basename='enrollments', viewset=EnrollmentApiViewSet)