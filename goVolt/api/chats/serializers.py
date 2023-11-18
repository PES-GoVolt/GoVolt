from rest_framework import serializers
from .models import Message,Chat

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender','content','timestamp','room_name']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['idUser','room_name','last_conection']