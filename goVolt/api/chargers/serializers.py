
from rest_framework import serializers
from .models import ChargerLocation,ChargerFullData

class ChargerLocationSerializer(serializers.ModelSerializer):
     class Meta:
        model = ChargerLocation
        fields = ['charger_id', 'latitude','longitude']

class ChargerFullDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargerFullData
        fields = ['charger_id', 'latitude', 'longitude', 'ac_dc', 'acces', 'adre_a', 'provincia', 'municipi', 'tipus_connexi']

