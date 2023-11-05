from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MessageSerializer
from .services import save_message
from rest_framework.response import Response


class ChatsAPIView(APIView):
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
    '''
    def get(self,request):
        group = request.data['room_name']
        return Response({'messages':get_all_messages(group)},status=status.HTTP_200_OK)

    '''