from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from role.api.serializers import RoleSerializer
from role.models import Role


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_roles_to_create_user_intern(request):
    try:
        roles = Role.objects.filter(deleted_at=None).exclude(name__in=["CLIENT", "DIRECTOR"])
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
