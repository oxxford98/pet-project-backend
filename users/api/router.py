from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

from users.api.views import (
    CustomTokenObtainPairView,
    UserApiViewSet,
    create_user_client,
    edit_user_client,
    get_info_user,
    request_password_reset,
    reset_password_with_code, get_client_user_stats, get_client_stats_enrollment_canine, get_client_stats_monthly_spends,
    get_director_stats_monthly_spends, get_global_monthly_enrollments_count, get_enrolled_by_size
)

router_user = DefaultRouter()
router_user.register(prefix="", basename="users", viewset=UserApiViewSet)

urlpatterns = [
    path("auth/login", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me", get_info_user),
    path("auth/password-reset/request", request_password_reset),
    path("auth/password-reset/confirm", reset_password_with_code),
    path("user/create-client", create_user_client),
    path("user/edit-client", edit_user_client),
    path("user/client-stats", get_client_user_stats),
    path("user/client-stats-enrollment-canine", get_client_stats_enrollment_canine),
    path("user/client-stats-monthly-spending", get_client_stats_monthly_spends),
    path("user/director-stats-monthly-spending", get_director_stats_monthly_spends),
    path("user/director-global-monthly-enrollments-count", get_global_monthly_enrollments_count),
    path("user/director-enrolled-by-size", get_enrolled_by_size),
]
