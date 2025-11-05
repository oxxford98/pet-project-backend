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
    reset_password_with_code,
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
]
