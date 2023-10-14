
from rest_framework import serializers
from .models import ChargerLocation

class ChargerLocationSerializer(serializers.ModelSerializer):
     class Meta:
        model = ChargerLocation
        fields = ['charger_id', 'latitude','longitude']