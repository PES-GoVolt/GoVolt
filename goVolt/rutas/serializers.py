from rest_framework import serializers
from .models import RutaViaje

class RutaViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutaViaje
        fields = '__all__'