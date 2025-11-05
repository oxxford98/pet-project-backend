from rest_framework import serializers

from canine.models import Canine


class CanineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canine
        fields = "__all__"
