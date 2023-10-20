
from firebase_admin import firestore
import pandas as pd
from sodapy import Socrata
from goVolt.settings import FIREBASE_DB
from .serializers import ChargerLocationSerializer
from rest_framework import serializers

def get_all_chargers():
    collection_ref = FIREBASE_DB.collection('charge_points')
    all_chargers = collection_ref.get()
    chargers_data = []
    for doc in all_chargers:
        data = doc.to_dict()
        data['charger_id'] = doc.id
        coordinates = data.get('geocoded_column',{}).get('coordinates',{})
        data['latitude'] = coordinates[0]
        data['longitude'] = coordinates[1]
        chargers_data.append(data)

    serializer = ChargerLocationSerializer(data=chargers_data, many=True)
    if serializer.is_valid():
        return serializer.data
    else:
        raise serializers.ValidationError(serializer.errors)



def get_chargers_by_codi_prov(codi_prov):
    collection_ref = FIREBASE_DB.collection('charge_points')
    query = collection_ref.where('codiprov','==',codi_prov)

    docs = query.get()

    result = []
    for doc in docs:
        data = doc.to_dict()
        result.append(data)
    return result

def store_charge_points_fb(data):
    collection_name = 'charge_points'
    collection_ref = FIREBASE_DB.collection(collection_name)

    for record in data:
        charger_id = record['id']
        existing_charger = collection_ref.document(str(charger_id)).get()

        if existing_charger.exists:
            existing_charger_data = existing_charger.to_dict()

            if existing_charger_data != record:
                existing_charger.reference.update(record)
        else:
            collection_ref.document(str(charger_id)).set(record)

def delete_all_charge_points_fb():
    collection_ref = FIREBASE_DB.collection('charge_points')
    docs = collection_ref.get()

    for doc in docs:
        doc.reference.delete()

def read_data():
    client = Socrata("analisi.transparenciacatalunya.cat", None)
    results = client.get("tb2m-m33b")
    results_df = pd.DataFrame.from_records(results)
    results_df = results_df[(results_df['acces'] != '') & (results_df['acces'] != 'APARCAMENT SEU (PRIVAT)')]
    results_df = results_df.to_dict(orient='records')
    return results_df 


