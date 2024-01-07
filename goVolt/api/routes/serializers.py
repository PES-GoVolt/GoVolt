from rest_framework import serializers

from .models import RutaViaje, RequestParticipant


class RutaViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutaViaje
        fields = ['ubicacion_inicial', 'ubicacion_final', 'precio', 'num_plazas', 'fecha', 'creador', 'participantes', 'username', 'nombreParticipantes']
        extra_kwargs = {
            'creador': {'required': False},
            'participantes': {'required': False},
            'nombreParticipantes': {'required': False}
        }

class RequestParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestParticipant
        fields = ['user_id', 'ruta_id', 'room_name']