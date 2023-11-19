from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class RutaViaje(models.Model):
    ubicacion_inicial = models.CharField(null=False, blank=False, max_length=300)
    ubicacion_final = models.CharField(null=False, blank=False, max_length=300)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    num_plazas = models.IntegerField(null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    creador = models.CharField(max_length=128, null=False, blank=False)
    participantes = ArrayField(models.CharField(max_length=128), blank=True, null=True)

    class Meta:
        db_table = 'rutas'

class RequestParticipant(models.Model):
    user_id = models.CharField(max_length=128, null=False, blank=False)
    ruta_id = models.CharField(max_length=128, null=False, blank=False)

    class Meta:
        db_table = 'requests_participants'
        unique_together = ('user_id', 'ruta_id')