from datetime import datetime, timedelta

import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from canine.models import Canine
from enrollment.models import Enrollment
from role.models import Role
from users.api.serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
)
from users.models import User
from users.utils import generate_verification_code, send_password_reset_email, user_has_any_role
from django.db.models import Sum, Count
from django.utils.timezone import now
from django.db.models.functions import ExtractMonth, ExtractYear


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        recaptcha_token = request.data.get("recaptcha")
        if not recaptcha_token:
            return Response(
                {"error": "Missing reCAPTCHA token"}, status=status.HTTP_400_BAD_REQUEST
            )

        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": recaptcha_token,
        }

        r = requests.post(verify_url, data=payload)
        result = r.json()

        if not result.get("success"):
            return Response({"error": "Invalid reCAPTCHA"}, status=status.HTTP_400_BAD_REQUEST)

        if result.get("score", 1) < 0.5:
            return Response(
                {"error": "Low reCAPTCHA score, suspected bot"}, status=status.HTTP_400_BAD_REQUEST
            )

        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data["email"])
        user_data = LoginSerializer(user).data

        response.data.update({"user": user_data})
        return response


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if not user_has_any_role(request.user.id, "DIRECTOR", "ADMIN"):
            return Response({"detail": "No allowed."}, status=status.HTTP_401_UNAUTHORIZED)

        role_id = request.data.get("role")

        role_name = (
            Role.objects.filter(id=role_id, deleted_at=None, name__in=["ADMIN", "TRAINER"])
            .values_list("name", flat=True)
            .first()
        )

        if not role_name:
            return Response(
                {
                    "detail": "El rol no existe o no está permitido. Solo se pueden crear usuarios con rol ADMIN o TRAINER."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "id": serializer.data["id"],
                "username": serializer.data["username"],
                "email": serializer.data["email"],
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if not user_has_any_role(request.user.id, "DIRECTOR", "ADMIN"):
            return Response({"detail": "No allowed."}, status=status.HTTP_401_UNAUTHORIZED)

        users = (
            User.objects.filter(deleted_at=None)
            .exclude(role__name__in=["DIRECTOR", "CLIENT"])
            .select_related("role")
        )

        serializer = LoginSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = LoginSerializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            password = request.data.get("password", None)
            if password:
                instance.set_password(password)
                instance.save()

            login_serializer = LoginSerializer(instance)
            return Response(login_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = LoginSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            password = request.data.get("password", None)
            if password:
                instance.set_password(password)
                instance.save()

            login_serializer = LoginSerializer(instance)
            return Response(login_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted_at = datetime.now()
        user.save()
        serializer = LoginSerializer(user)
        data = {
            "status": "ok",
        }
        return Response(data=data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_info_user(request):
    user = request.user
    serializer = LoginSerializer(user)
    response_data = serializer.data

    return Response(response_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_user_client(request):
    data = request.data.copy()
    data["username"] = data.get("email", "")
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        role_client = get_object_or_404(Role, name=Role.CLIENT)

        user = serializer.save(role=role_client)
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.name,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def edit_user_client(request):
    id_user = request.user.id
    instance = get_object_or_404(User, id=id_user, deleted_at=None)

    request_data = request.data.copy()
    if "role" in request_data:
        request_data.pop("role")

    serializer = LoginSerializer(instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        password = request.data.get("password", None)
        if password:
            instance.set_password(password)
            instance.save()

        login_serializer = LoginSerializer(instance)
        return Response(login_serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    """
    Endpoint para solicitar el código de verificación para reset de contraseña.
    Envía un email con el código de verificación.
    """
    serializer = PasswordResetRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data["email"]

    try:
        user = User.objects.get(email=email, deleted_at=None)
    except User.DoesNotExist:
        return Response(
            {"error": "Error al enviar el email. Usuario no existe"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Generar código de verificación
    verify_code = generate_verification_code()

    # Guardar código en el usuario con timestamp
    user.verify_code = verify_code
    user.updated_at = timezone.now()
    user.save(update_fields=["verify_code", "updated_at"])

    # Enviar email
    email_sent = send_password_reset_email(user, verify_code)

    if email_sent:
        return Response(
            {"message": "Código de verificación enviado al email"}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Error al enviar el email. Intenta nuevamente"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_with_code(request):
    """
    Endpoint para validar el código de verificación y establecer nueva contraseña.
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data["email"]
    verify_code = serializer.validated_data["verify_code"]
    new_password = serializer.validated_data["new_password"]

    try:
        user = User.objects.get(email=email, deleted_at=None)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Verificar que el código coincida
    if user.verify_code != verify_code:
        return Response(
            {"error": "Código de verificación inválido"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Verificar que el código no haya expirado (30 minutos)
    time_diff = timezone.now() - user.updated_at
    if time_diff > timedelta(minutes=30):
        return Response(
            {"error": "El código de verificación ha expirado"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Actualizar contraseña y limpiar código de verificación
    user.set_password(new_password)
    user.verify_code = None
    user.save(update_fields=["password", "verify_code"])

    return Response({"message": "Contraseña actualizada exitosamente"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_client_user_stats(request):
    user = request.user

    pets = Canine.objects.filter(
        user=user,
        deleted_at=None
    )

    total_pets = pets.count()

    pet_ids = pets.values_list("id", flat=True)

    active_enrollments = Enrollment.objects.filter(
        canine_id__in=pet_ids,
        is_active=True,
        deleted_at=None
    )

    enrolled_pets = active_enrollments.count()

    pending_enrollment = total_pets - enrolled_pets

    total_spent_2025 = (
        active_enrollments
        .filter(start_date__year=2025)
        .aggregate(total=Sum("plan__price"))
        .get("total")
    )

    total_spent_2025 = total_spent_2025 or 0

    response = {
        "total_pets": total_pets,
        "enrolled_pets": enrolled_pets,
        "pending_enrollment": pending_enrollment,
        "total_spent_2025": total_spent_2025
    }

    return Response(response)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_client_stats_enrollment_canine(request):
    user = request.user
    today = now().date()

    pets = Canine.objects.filter(user=user, deleted_at=None)
    pet_ids = pets.values_list("id", flat=True)

    active_enrollments = Enrollment.objects.select_related("canine", "plan").filter(
        canine_id__in=pet_ids,
        is_active=True,
        deleted_at=None
    )

    response = []

    for enr in active_enrollments:
        end_date = enr.end_date

        days_until_expiration = (end_date - today).days

        response.append({
            "canine_id": enr.canine.id,
            "canine_name": enr.canine.name,
            "plan_name": enr.plan.name,
            "end_date": end_date,
            "days_until_expiration": days_until_expiration
        })

    return Response(response)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_client_stats_monthly_spends(request):
    try:
        year = int(request.GET.get("year"))
    except:
        return Response({"detail": "Debe enviar year como número."}, status=400)

    user = request.user

    canines = Canine.objects.filter(user=user, deleted_at=None)
    pet_ids = canines.values_list("id", flat=True)

    enrollments = (
        Enrollment.objects.filter(
            canine_id__in=pet_ids,
            deleted_at=None,
            start_date__year=year,
        )
        .annotate(month=ExtractMonth("start_date"))
        .select_related("plan")
        .values("month")
        .annotate(amount=Sum("plan__price"))
        .order_by("month")
    )

    monthly_map = {item["month"]: item["amount"] for item in enrollments}

    monthly_data = []
    for m in range(1, 13):
        monthly_data.append({
            "month": m,
            "amount": monthly_map.get(m, 0)
        })

    return Response({
        "year": year,
        "monthly_data": monthly_data
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_director_stats_monthly_spends(request):
    year = timezone.now().year

    enrollments = (
        Enrollment.objects.filter(
            deleted_at=None,
            start_date__year=year,
        )
        .annotate(month=ExtractMonth("start_date"))
        .values("month")
        .annotate(amount=Sum("plan__price"))
        .order_by("month")
    )

    monthly_map = {item["month"]: item["amount"] for item in enrollments}

    monthly_data = []
    for m in range(1, 13):
        monthly_data.append({
            "month": m,
            "amount": monthly_map.get(m, 0)
        })

    return Response({
        "monthly_data": monthly_data
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_global_monthly_enrollments_count(request):
    year = timezone.now().year

    enrollments = (
        Enrollment.objects.filter(
            deleted_at=None,
            start_date__year=year,
        )
        .annotate(month=ExtractMonth("start_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    monthly_map = {item["month"]: item["count"] for item in enrollments}

    monthly_data = []
    for m in range(1, 13):
        monthly_data.append({
            "month": m,
            "count": monthly_map.get(m, 0)
        })

    return Response({
        "monthly_data": monthly_data
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_enrolled_by_size(request):

    data = (
        Enrollment.objects.filter(
            is_active=True,
            deleted_at=None
        )
        .values("canine__size")
        .annotate(total=Count("id"))
    )

    size_map = {
        1: "small",
        2: "medium",
        3: "large"
    }

    response = {
        "small": 0,
        "medium": 0,
        "large": 0
    }

    for item in data:
        size = item["canine__size"]
        count = item["total"]
        response[size_map[size]] = count

    return Response(response)