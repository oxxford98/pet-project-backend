from rest_framework.views import APIView
from users.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.api.serializers import LoginSerializer, RegisterSerializer
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from role.models import Role
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.utils import user_has_any_role


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data['email'])
        user_data = LoginSerializer(user).data

        response.data.update({'user': user_data})
        return response


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if not user_has_any_role(request.user.id, "DIRECTOR", "ADMIN"):
            return Response(
                {'detail': 'No allowed.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        role_id = request.data.get('role')

        role_name = Role.objects.filter(
            id=role_id,
            deleted_at=None,
            name__in=['ADMIN', 'TRAINER']
        ).values_list('name', flat=True).first()

        if not role_name:
            return Response(
                {
                    'detail': 'El rol no existe o no está permitido. Solo se pueden crear usuarios con rol ADMIN o TRAINER.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'id': serializer.data['id'],
                'username': serializer.data['username'],
                'email': serializer.data['email'],
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if not user_has_any_role(request.user.id, "DIRECTOR", "ADMIN"):
            return Response(
                {'detail': 'No allowed.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        users = User.objects.filter(
            deleted_at=None
        ).exclude(
            role__name__in=['DIRECTOR', 'CLIENT']
        ).select_related('role')

        serializer = LoginSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = LoginSerializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            password = request.data.get('password', None)
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
            password = request.data.get('password', None)
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
            'status': 'ok',

        }
        return Response(data=data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_info_user(request):
    user = request.user
    serializer = LoginSerializer(user)
    response_data = serializer.data

    return Response(response_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_client(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        role_client = get_object_or_404(Role, name=Role.CLIENT)

        user = serializer.save(role=role_client)
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.name
        }
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_user_client(request, id_user):
    instance = get_object_or_404(User, id=id_user, deleted_at=None)

    request_data = request.data.copy()
    if 'role' in request_data:
        request_data.pop('role')

    serializer = LoginSerializer(instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        password = request.data.get('password', None)
        if password:
            instance.set_password(password)
            instance.save()

        login_serializer = LoginSerializer(instance)
        return Response(login_serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)