import requests
import json
from goVolt.settings import FIREBASE_DB
from firebase_admin import firestore
from .serializers import BikestationLocationSerializer

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

def get_all_bikestations():
    collection_ref = FIREBASE_DB.collection('bike_stations')
    docs = collection_ref.get()


    chargers_data = []
    for doc in docs:
        data = doc.to_dict()
        data['station_id'] = doc.id
        data['latitude'] = data.get('lat',{})
        data['longitude'] = data.get('lon',{})
        chargers_data.append(data)

    serializer = BikestationLocationSerializer(data=chargers_data, many=True)
    if serializer.is_valid():
        return serializer.data
    else:
        raise serializers.ValidationError(serializer.errors)