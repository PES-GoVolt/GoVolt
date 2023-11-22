from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):

    # Agrega campos personalizados aquí
    first_name = models.CharField(max_length=30, null=True, default=None)
    last_name = models.CharField(max_length=30, null=True, default=None)
    photo_url = models.URLField(blank=True, null=True, default=None)
    # Campo para almacenar el UID de Firebase
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, default=None)
    phone = models.CharField(max_length=30, null=True, default=None)
    email = models.CharField(max_length=30, null=True, default=None)

    # Especifica nombres de acceso inverso personalizados para los campos de grupos y permisos
    groups = models.ManyToManyField('auth.Group', related_name='custom_users')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_users')

    # Especifica el nombre de la tabla en la base de datos
    class Meta:
        db_table = 'users'