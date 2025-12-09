"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.contrib import admin
from django.urls import include, path, re_path

from canine.api.router import router_canine
from enrollment.api.router import router_enrollment
from plan.api.router import router_plan
from users.api.router import router_user
from attendance.api.router import router_attendance

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/", include("users.api.router")),
    path("api/", include("role.api.router")),
    path("api/", include("canine.api.router")),
    path("api/", include("enrollment.api.router")),
    path("admin/", admin.site.urls),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redocs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/user/", include(router_user.urls)),
    path("api/canine/", include(router_canine.urls)),
    path("api/plan/", include(router_plan.urls)),
    path("api/enrollment/", include(router_enrollment.urls)),
    path("api/attendance/", include(router_attendance.urls)),
]
