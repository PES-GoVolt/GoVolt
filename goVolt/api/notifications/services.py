from goVolt.settings import FIREBASE_DB,AUTH_DB
from datetime import datetime
import warnings
from firebase_admin import db,auth
import json
from .utils import get_timestamp_now
from .serializers import NotificationSerializer
from rest_framework import serializers
from google.cloud import firestore
from rest_framework.response import Response

def save_notification(notification,user_id):
    try:
        ref = db.reference("/")

        current_datetime = datetime.now()
        unix_timestamp = int(current_datetime.timestamp() * 1000)

        notificationdata = {
            "content": notification,
            "timestamp": unix_timestamp
        }
        notification_node = ref.child("notifications/"+user_id).push()
        notification_node.set(notificationdata)

        return Response({'message': "Notification created successfully."}, status=201)
    
    except Exception as e:
        return Response({'message': str(e)}, status=400)


def get_user_notifications(firebase_token):
    decoded_token = auth.verify_id_token(firebase_token)
    user_id = decoded_token['uid']

    ref = db.reference('notifications/'+user_id+'/')
    notifications_data = ref.get()

    notifications = []
    if notifications_data:
        for notification_id, notification_info in notifications_data.items():
            print(notification_info)
            if 'content' in notification_info:
                notification = {
                    'content': notification_info['content'],
                    'timestamp': notification_info['timestamp']
                }
                notifications.append(notification)
        notifications = sorted(notifications, key=lambda x: x['timestamp'])
        serializer = NotificationSerializer(data=notifications,many=True)
        if serializer.is_valid():
            return serializer.data
        else:
            raise serializers.ValidationError(serializer.errors)
    return notifications
