from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import NotificationSerializer
from .services import save_notification,get_user_notifications
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from api.users.authentication import FirebaseAuthentication

class NotificationsAPIView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]
    
    def post(self,request):
        data = request.data
        notification = data['content']
        user_id = data['user_id']

        save_notification(notification, user_id)
        return Response({'message':'Notification created'},status=status.HTTP_201_CREATED)
    
    def get(self,request):
        user_id = request.query_params.get('user_id','')
        notifications = get_user_notifications(user_id)
        return Response({'notifications':notifications},status=status.HTTP_200_OK)
    