from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from enrollment.models import Enrollment
from enrollment.api.serializers import EnrollmentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from plan.models import Plan
from datetime import date
from dateutil.relativedelta import relativedelta


class EnrollmentApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()

    def create(self, request, *args, **kwargs):
        plan_id = request.data.get('plan')

        try:
            plan = Plan.objects.get(id=plan_id, deleted_at=None)
        except Plan.DoesNotExist:
            return Response(
                {'error': 'Plan not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        start_date = date.today()

        months = plan.duration_days // 30

        end_date = start_date + relativedelta(months=months)

        request.data['start_date'] = start_date
        request.data['end_date'] = end_date
        request.data['is_active'] = True

        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)