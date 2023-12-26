from firebase_admin import firestore
import pandas as pd
from sodapy import Socrata
from rest_framework import serializers
from goVolt.settings import AUTH_DB
from goVolt.settings import FIREBASE_DB
from firebase_admin import auth, exceptions
from .serializers import UserSerializer
from rest_framework.exceptions import ValidationError
import json
from rest_framework.response import Response


def store_user(firebase_token, email, phone, username):
    # Crea una cuenta de usuario en Firebase Authentication
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        firebase_uid = decoded_token['uid']

        # insertar usuarios en la bbdd
        collection_name = 'users'
        user_data = {
            'first_name': None,
            'last_name': None,
            'photo_url': None,
            'phone': phone,
            'email': email,
            'username': username,
            'firebase_uid': firebase_uid
        }

        collection_ref = FIREBASE_DB.collection(collection_name)
        # Crea un documento con el ID del usuario (UID) y almacena los datos
        collection_ref.document(firebase_uid).set(user_data)

        # user = FIREBASE_DB.collection('users').document(firebase_uid).get()
        return Response({'message': "OK"}, status=200)
    except Exception as e:

        return Response({'message': str(e)}, status=400)


def get_see_my_profile(firebase_token):
    # Obten el token de autenticación de la solicitud

    decoded_token = auth.verify_id_token(firebase_token)
    firebase_uid = decoded_token['uid']
    
    user_ref = FIREBASE_DB.collection('users').document(firebase_uid)
    res = user_ref.get()

    data = {}
    data['username'] = res.get('username')
    data['first_name'] = res.get('first_name')
    data['last_name'] = res.get('last_name')
    data['photo_url'] = res.get('photo_url')
    data['phone'] = res.get('phone')
    data['email'] = res.get('email')

    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        print(serializer.data)
        return serializer.data
    else:
        print(serializer.errors)
        raise ValidationError(serializer.errors)

def has_info_external(firebase_token):
    decoded_token = auth.verify_id_token(firebase_token)
    firebase_uid = decoded_token['uid']

    user_ref = FIREBASE_DB.collection('users').document(firebase_uid)
    res = user_ref.get()

    # Verifica si el documento existe
    data = res.to_dict()

    if data:
        data['username'] = data.get('username', None)
        data['phone'] = data.get('phone', None)
        data['email'] = data.get('email', None)

        if (data['username'] == None or data['phone'] == None or data['email'] == None):
            return False
        else:
            return True
    else:
        return False

def empty_string_to_none(value):
    return None if value == "" else value

def edit_user(firebase_token, first_name, last_name, phone, photo_url):

    # Crea una cuenta de usuario en Firebase Authentication
    try:

        decoded_token = auth.verify_id_token(firebase_token)
        firebase_uid = decoded_token['uid']

        user_ref = FIREBASE_DB.collection('users').document(firebase_uid)

        first_name = empty_string_to_none(first_name)
        last_name = empty_string_to_none(last_name)
        phone = empty_string_to_none(phone)
        photo_url = empty_string_to_none(photo_url)

        user_ref.update({
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'photo_url': photo_url,
        })

        return Response({'message': "OK"}, status=200)
    except Exception as e:
        error_message = e.args[1]
        error_data = json.loads(error_message)

        code = error_data['error']['code']
        msg = error_data['error']['message']

        return Response({'message': msg}, status=code)
