import json

import requests

from goVolt.settings import FIREBASE_DB
from .serializers import BikestationLocationSerializer

URL_API_BIKES = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'



def read_data_stations():
    data = requests.get(URL_API_BIKES)
    data_json = json.loads(data.content.decode('utf-8'))
    return data_json['data']['stations']

def store_data_stations(data):
    collection_name = 'bike_stations'
    collection_ref = FIREBASE_DB.collection(collection_name)

    for record in data:
        station_id = record['station_id']
        existing_station = collection_ref.document(str(station_id)).get()

        if existing_station.exists:
            existing_station_data = existing_station.to_dict()

            if existing_station_data != record:
                existing_station.reference.update(record)
        else:
            collection_ref.document(str(station_id)).set(record)

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
        raise serializer.ValidationError(serializer.errors)