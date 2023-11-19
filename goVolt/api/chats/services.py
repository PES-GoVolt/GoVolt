from goVolt.settings import FIREBASE_DB_REALTIME_URL
from datetime import datetime

from firebase_admin import db
import json

def save_message(message,room_name,sender):
    ref = db.reference("/")

    current_datetime = datetime.now()
    unix_timestamp = int(current_datetime.timestamp() * 1000)

    messagedata = {
        "content": message,
        "room_name": room_name,
        "sender": sender,
        "timestamp": unix_timestamp
    }
    message_node = ref.child(room_name).push()
    message_node.set(messagedata)


def get_room_messages(room_name):
    ref = db.reference('/' + room_name)
    messages_data = ref.get()
    messages = []
    if messages_data:
            for message_id, message_info in messages_data.items():
                if 'content' in message_info:
                    message = {
                        'content': message_info['content'],
                        'room_name': message_info['room_name'],
                        'sender': message_info['sender'],
                        'timestamp': message_info['timestamp']
                    }
                    messages.append(message)
            messages = sorted(messages, key=lambda x: x['timestamp'])
    return messages


    