from datetime import date

from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from enrollment.api.serializers import EnrollmentSerializer
from enrollment.models import Enrollment
from plan.models import Plan


class EnrollmentApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()

    def create(self, request, *args, **kwargs):
        plan_id = request.data.get("plan")

        try:
            plan = Plan.objects.get(id=plan_id, deleted_at=None)
        except Plan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        start_date = date.today()

        months = plan.duration_days // 30

        end_date = start_date + relativedelta(months=months)

        request.data["start_date"] = start_date
        request.data["end_date"] = end_date
        request.data["is_active"] = True

        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = date.today()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_enrollment_active_by_canine(request, canine_id):
    try:
        enrollment = Enrollment.objects.select_related("plan", "canine").get(
            canine=canine_id, is_active=True, deleted_at=None
        )
    except Enrollment.DoesNotExist:
        return Response(
            {"error": "Active enrollment not found for the specified canine"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = EnrollmentSerializer(enrollment)
    data = dict(serializer.data)

    plan = enrollment.plan
    canine = enrollment.canine

    data["plan"] = {
        "id": plan.id,
        "name": plan.name,
        "description": plan.description,
        "duration_days": plan.duration_days,
        "transport_type": plan.transport_type,
        "price": str(plan.price),
    }

    data["canine"] = {
        "id": canine.id,
        "name": canine.name,
        "breed": canine.breed,
        "size": canine.size,
        "birth_date": canine.birth_date,
        "user_id": canine.user_id,
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_enrollment_active_to_director(request):
    data = request.data

    size = data.get("size")
    breed = data.get("breed")
    plan_id = data.get("plan")

    queryset = Enrollment.objects.select_related("canine", "plan").filter(
        is_active=True,
        deleted_at=None
    )

    if size:
        queryset = queryset.filter(canine__size=size)

    if breed:
        queryset = queryset.filter(canine__breed__icontains=breed)

    if plan_id:
        queryset = queryset.filter(plan_id=plan_id)

    response = []

    for enrollment in queryset:
        response.append({
            "id": enrollment.id,
            "start_date": enrollment.start_date,
            "end_date": enrollment.end_date,
            "is_active": enrollment.is_active,
            "created_at": enrollment.created_at,
            "updated_at": enrollment.updated_at,

            "canine": {
                "id": enrollment.canine.id,
                "name": enrollment.canine.name,
                "breed": enrollment.canine.breed,
                "size": enrollment.canine.size,
                "birth_date": enrollment.canine.birth_date,
                "user_id": enrollment.canine.user_id,
                "created_at": enrollment.canine.created_at,
                "updated_at": enrollment.canine.updated_at,
            },
            "plan": {
                "id": enrollment.plan.id,
                "name": enrollment.plan.name,
                "description": enrollment.plan.description,
                "duration_days": enrollment.plan.duration_days,
                "transport_type": enrollment.plan.transport_type,
                "price": str(enrollment.plan.price),
                "created_at": enrollment.plan.created_at,
                "updated_at": enrollment.plan.updated_at,
            }
        })

    return Response(response)