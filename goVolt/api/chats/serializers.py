from rest_framework import serializers

from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender','content','timestamp','room_name']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id_chat','idUser_sender','idUser_reciever','email','room_name','last_conection','creator']