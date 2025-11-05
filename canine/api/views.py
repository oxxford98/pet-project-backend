from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db.models import Exists, OuterRef

from canine.api.serializers import CanineSerializer
from canine.models import Canine
from enrollment.models import Enrollment
from users.utils import user_has_any_role


class CanineApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CanineSerializer
    queryset = Canine.objects.all()

    def create(self, request, *args, **kwargs):
        if not user_has_any_role(request.user.id, "CLIENT"):
            return Response({"detail": "No allowed."}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data["user"] = request.user.id
        serializer = CanineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_canine_by_client(request):
    if not user_has_any_role(request.user.id, "CLIENT"):
        return Response({"detail": "No allowed."}, status=status.HTTP_401_UNAUTHORIZED)

    active_enrollment = Enrollment.objects.filter(
        canine=OuterRef("pk"), is_active=True, deleted_at=None
    )

    canines = Canine.objects.filter(user=request.user, deleted_at=None).annotate(
        is_matriculated=Exists(active_enrollment)
    )

    serializer = CanineSerializer(canines, many=True)

    response_data = serializer.data
    for idx, canine in enumerate(canines):
        response_data[idx]["is_matriculated"] = canine.is_matriculated

    return Response(response_data, status=status.HTTP_200_OK)
