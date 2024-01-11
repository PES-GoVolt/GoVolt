import pandas as pd
from firebase_admin import auth
from firebase_admin import firestore
from rest_framework import serializers
from sodapy import Socrata

from goVolt.settings import FIREBASE_DB
from .serializers import ChargerFullDataSerializer


def get_all_chargers():
    collection_ref = FIREBASE_DB.collection('charge_points')
    all_chargers = collection_ref.get()
    chargers_data = []
    for doc in all_chargers:
        data = doc.to_dict()
        data['charger_id'] = doc.id
        coordinates = data.get('geocoded_column', {}).get('coordinates', {})
        data['latitude'] = coordinates[0]
        data['longitude'] = coordinates[1]
        address = str(data["adre_a"])
        connex = str(data["tipus_connexi"])
        if (address is not None and len(address) != 0) and (connex is not None and len(connex) != 0):
            chargers_data.append(data)
    serializer = ChargerFullDataSerializer(data=chargers_data, many=True)
    if serializer.is_valid():
        return serializer.data
    else:
        raise serializers.ValidationError(serializer.errors)


def increment_nearest_charger_achievement(firebase_token):
    decoded_token = auth.verify_id_token(firebase_token)
    logged_uid = decoded_token['uid']
    collection_name = 'users'
    user_ref = FIREBASE_DB.collection(collection_name).document(logged_uid)
    user_ref.update({
        "nearest_charger_achievement": firestore.Increment(1)
    })


def get_charger_by_id(id):
    doc_ref = FIREBASE_DB.collection('charge_points').document(id)

    res = doc_ref.get()

    data = {}
    data['charger_id'] = id
    data['latitude'] = res.get('latitud')
    data['longitude'] = res.get('longitud')
    data['ac_dc'] = res.get('ac_dc')
    data['acces'] = res.get('acces')
    data['adre_a'] = res.get('adre_a')
    data['provincia'] = res.get('codiprov')
    data['municipi'] = res.get('municipi')
    data['charger_speed'] = res.get('tipus_velocitat')
    data['tipus_connexi'] = res.get('tipus_connexi')

    serializer = ChargerFullDataSerializer(data=data, many=False)
    if serializer.is_valid():
        return serializer.data

    else:
        raise serializers.ValidationError(serializer.errors)


def get_chargers_by_codi_prov(codi_prov):
    collection_ref = FIREBASE_DB.collection('charge_points')
    query = collection_ref.where('codiprov', '==', codi_prov)

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
