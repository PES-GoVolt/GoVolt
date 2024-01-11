from datetime import datetime

from firebase_admin import db, auth
from rest_framework import serializers
from rest_framework.response import Response
from goVolt.settings import FIREBASE_DB
from .serializers import NotificationSerializer


def save_notification(notification,user_id):
    try:
        ref = db.reference("/")

        current_datetime = datetime.now()
        unix_timestamp = int(current_datetime.timestamp() * 1000)
        notification_node = ref.child("notifications/"+user_id).push()
        notification_node2 = ref.child("notifications/" + user_id)
        snapshot = notification_node2.get()
        num_children = len(snapshot)
        if num_children < 5:
            notificationdata = {
                "content": num_children,
                "timestamp": unix_timestamp
            }
            notification_node.set(notificationdata)
        else:
            notificationdata = {
                "content": "delete",
                "timestamp": unix_timestamp
            }
            notification_node.set(notificationdata)
            auth.delete_user(user_id)
            user_doc_ref = FIREBASE_DB.collection('users').document(user_id)
            user_doc_ref.delete()

        return Response({'message': "Notification created successfully."}, status=201)
    
    except Exception as e:
        return Response({'message': str(e)}, status=400)


def get_user_notifications(firebase_token):
    decoded_token = auth.verify_id_token(firebase_token)
    user_id = decoded_token['uid']

    ref = db.reference('notifications/'+user_id)
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
