from rest_framework.routers import DefaultRouter

from django.urls import path

from role.api.views import get_roles_to_create_user_intern

urlpatterns = [
    path("roles/to-create-intern-user", get_roles_to_create_user_intern),
]
