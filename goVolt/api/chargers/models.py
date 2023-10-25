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
    address = models.CharField(max_length=200)
    province_code = models.CharField(max_length=100)
    mun = models.CharField(max_length=100)
    charger_speed = models.CharField(max_length=100)
    conection_type = models.CharField(max_length=200)

