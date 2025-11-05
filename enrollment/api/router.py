from rest_framework.routers import DefaultRouter

from django.urls import path

from enrollment.api.views import EnrollmentApiViewSet, get_enrollment_active_by_canine

router_enrollment = DefaultRouter()
router_enrollment.register(prefix="", basename="enrollments", viewset=EnrollmentApiViewSet)


urlpatterns = [
    path("enrollment/by-canine/<canine_id>", get_enrollment_active_by_canine),
]
