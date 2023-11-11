from django.db import models
from api.users.models import CustomUser
# Create your models here.

class RutaViaje(models.Model):
    ubicacion_inicial = models.CharField(null=False, blank=False, max_length=300)
    ubicacion_final = models.CharField(null=False, blank=False, max_length=300)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    num_plazas = models.IntegerField(null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    creador = models.CharField(max_length=128, null=False, blank=False)
    participantes = models.ManyToManyField(CustomUser, related_name='participantes', blank=True)

    class Meta:
        db_table = 'rutas'