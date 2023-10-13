from django.db import models

class ChargerLocation(models.Model):
    
    latitude = models.FloatField(null=True,blank=False)
    longitude = models.FloatField(null=True,blank=False)

    def __str__(self):
        return self.latitude,self.longitude