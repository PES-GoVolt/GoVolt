from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MessageSerializer
from .services import save_message,get_room_messages,modify_timestamp_chat,save_chat,get_chats_user_loged
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from api.users.autentication import FirebaseAuthentication

class MessagesAPIView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]
    def post(self,request):
        data = request.data
        message = data['content']
        room_name = data['room_name']
        sender = data['sender']
        save_message(message,room_name,sender)
        return Response({'message':'Message created'},status=status.HTTP_201_CREATED)
    
    def get(self,request):
        room = request.query_params.get('room_name','')
        messages = get_room_messages(room)
        return Response({'messages':messages},status=status.HTTP_200_OK)
    

from firebase_admin import auth
class ChatsAPIView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]
    def put(self,request):
        id_chat = request.data['id_chat']
        modify_timestamp_chat(id_chat)
        return Response({'message':'Timestamp updated'},status=status.HTTP_200_OK)

    def post(self,request):
        uid = request.data['user_uid']
        room_name = request.data['room_name']
        creator_uid = request.data['creator_uid']
        room_name = save_chat(uid,room_name,creator_uid)
        return Response({'message' : 'Chat created ', "room_name" : room_name},status=status.HTTP_201_CREATED)

    def get(self,request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        decoded_token = auth.verify_id_token(firebase_token)
        uid = decoded_token['uid']
        chats = get_chats_user_loged(uid)
        return Response({'chats':chats},status=status.HTTP_200_OK)



