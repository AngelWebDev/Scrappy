from rest_framework import serializers
from .models import Arrival, Material


class ArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrival
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

