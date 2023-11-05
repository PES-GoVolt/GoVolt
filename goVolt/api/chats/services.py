from goVolt.settings import FIREBASE_DB_REALTIME_URL
from datetime import datetime

from firebase_admin import db
import json

def save_message(message,room_name,sender):
    ref = db.reference("/")

    current_datetime = datetime.now()
    unix_timestamp = current_datetime.timestamp()

    messagedata = {
        "content": message,
        "room_name": room_name,
        "sender": sender,
        "timestamp": unix_timestamp
    }
    message_node = ref.child(room_name).push()
    message_node.set(messagedata)








    