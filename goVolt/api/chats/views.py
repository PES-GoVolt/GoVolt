from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.authentication import FirebaseAuthentication
from .services import save_message, get_room_messages, modify_timestamp_chat, save_chat, get_chats_user_loged


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
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        room_name = save_chat(uid,room_name,creator_uid,firebase_token)
        if (room_name == "error1"):
            return Response({'message': 'PARTICIPANT ALREADY EXIST'}, status=status.HTTP_400_BAD_REQUEST)
        if (room_name == "error2"):
            return Response({'message': 'THE REQUEST ALREADY EXIST'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message' : 'Chat created ', "room_name" : room_name},status=status.HTTP_201_CREATED)

    def get(self,request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        chats = get_chats_user_loged(firebase_token)
        return Response({'chats':chats},status=status.HTTP_200_OK)



