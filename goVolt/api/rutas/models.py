from django.db import models

# Create your models here.

class RutaViaje(models.Model):
    ubicacion_inicial = models.CharField(null=False,blank=False,max_length=300)
    ubicacion_final = models.CharField(null=False,blank=False,max_length=300)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    num_plazas = models.IntegerField(null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)

    class Meta:
        db_table = 'rutas'