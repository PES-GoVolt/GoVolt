from django.db import models

# Create your models here.


class BikestationLocation(models.Model):
    station_id = models.CharField(null=False,blank=False,max_length=100)
    latitude = models.FloatField(null=True,blank=False)
    longitude = models.FloatField(null=True,blank=False)

    def __str__(self):
        return self.latitude,self.longitude