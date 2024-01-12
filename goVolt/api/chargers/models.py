from django.db import models

class ChargerLocation(models.Model):
    charger_id = models.CharField(null=False,blank=False,max_length=100)
    latitude = models.FloatField(null=True,blank=False)
    longitude = models.FloatField(null=True,blank=False)

    def __str__(self):
        return self.latitude,self.longitude
    

class ChargerFullData(models.Model):
    charger_id = models.CharField(null=False,blank=False,max_length=100)
    latitude = models.FloatField(null=True,blank=False)
    longitude = models.FloatField(null=True,blank=False)
    ac_dc = models.CharField(max_length=100)
    acces = models.CharField(max_length=100)
    adre_a = models.CharField(max_length=200)
    provincia = models.CharField(max_length=100)
    municipi = models.CharField(max_length=100)
    tipus_connexi = models.CharField(max_length=100)

