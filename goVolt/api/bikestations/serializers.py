from rest_framework import serializers
from .models import BikestationLocation

class BikestationLocationSerializer(serializers.ModelSerializer):
     class Meta:
        model = BikestationLocation
        fields = ['station_id', 'latitude','longitude', 'address']