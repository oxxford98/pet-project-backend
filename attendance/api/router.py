from rest_framework.routers import DefaultRouter
from django.urls import path
from attendance.api.views import AttendanceApiViewSet

router_attendance = DefaultRouter()
router_attendance.register(prefix="", basename="attendances", viewset=AttendanceApiViewSet)