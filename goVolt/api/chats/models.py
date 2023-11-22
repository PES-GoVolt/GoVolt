from django.db import models

# Create your models here.


class Message(models.Model):
    sender = models.CharField(max_length=100) # Aqui ira la fk cuando este hecho lo de usuarios
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=100)


