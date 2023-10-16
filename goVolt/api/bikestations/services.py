import requests
import json
from goVolt.settings import FIREBASE_DB
from firebase_admin import firestore

URL_API_BIKES = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'



def read_data_stations():
    data = requests.get(URL_API_BIKES)
    data_json = json.loads(data.content.decode('utf-8'))
    return data_json['data']['stations']

def store_data_stations(data):
    collection_name = 'bike_stations'

    for record in data:
        FIREBASE_DB.collection(collection_name).add(record)

def delete_all_bikestations_fb():
    collection_ref = FIREBASE_DB.collection('bike_stations')
    docs = collection_ref.get()
    for doc in docs:
        doc.reference.delete()