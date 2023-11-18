from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MessageSerializer
from .services import save_message,get_room_messages,modify_timestamp_chat,save_chat,get_chat
from rest_framework.response import Response


class MessagesAPIView(APIView):
    def post(self,request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            message = data['content']
            room_name = data['room_name']
            sender = data['sender']
            save_message(message,room_name,sender)
            return Response({'message':'Message created'},status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    
    def get(self,request):
        room = request.query_params.get('room_name','')
        messages = get_room_messages(room)
        return Response({'messages':messages},status=status.HTTP_200_OK)

class ChatsAPIView(APIView):
    def put(self,request):
        id_chat = request.data['id_chat']
        modify_timestamp_chat(id_chat)
        return Response({'message':'Timestamp updated'},status=status.HTTP_200_OK)#modificar timestamp al actual

    def post(self,request):
        uid = request.data['user_uid']
        room_name = request.data['room_name']
        save_chat(uid,room_name)
        # me pasa uid y room name timestamp->now // crearotro para el usuario logeado
        return Response({'message' : 'Chat created'},status=status.HTTP_201_CREATED)

    def get(self,request):
        id_chat = request.query_params.get('id_chat','')
        chats = get_chat(id_chat)

        return Response({'chats':chats},status=status.HTTP_200_OK)
        #devolver todo para el usuario loged


