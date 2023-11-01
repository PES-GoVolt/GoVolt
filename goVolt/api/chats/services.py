from goVolt.settings import FIREBASE_DB
from google.cloud import firestore
from datetime import datetime

def save_message(message):
    collection_name = 'messages'
    collection_ref = FIREBASE_DB.collection(collection_name)


    current_datetime = datetime.now()

    messagedata = {
        "content": message['content'],
        "room_name": message['room_name'],
        "sender": message['sender'],
        "timestamp": current_datetime
    }
    collection_ref.add(messagedata)

def get_all_messages(room_name):
    collection_name = 'messages'
    collection_ref = FIREBASE_DB.collection(collection_name)

    query = collection_ref.where('room_name','==',room_name).order_by('timestamp')
    docs = query.stream()

    messages = []

    for doc in docs:
        doc_data = doc.to_dict()
        messages.append(doc_data)  
    return messages