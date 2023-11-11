from rest_framework import serializers
from .models import RutaViaje

class RutaViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutaViaje
        fields = ['ubicacion_inicial', 'ubicacion_final', 'precio', 'num_plazas', 'fecha', 'creador', 'participantes']
        extra_kwargs = {
            'creador': {'required': False},
            'participantes': {'required': False}
        }