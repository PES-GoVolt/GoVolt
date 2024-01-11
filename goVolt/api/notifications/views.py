from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
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

        result = save_notification(notification, user_id)

        if (result.status_code != 201):
            code = result.status_code

            if code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": result.data.get('message')}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message': result.data.get('message')}, status=status.HTTP_201_CREATED)
    
    def get(self,request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        notifications = get_user_notifications(firebase_token)
        return Response({'notifications':notifications},status=status.HTTP_200_OK)
    