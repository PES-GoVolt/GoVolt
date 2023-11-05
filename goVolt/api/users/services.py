
from firebase_admin import firestore
import pandas as pd
from sodapy import Socrata
from rest_framework import serializers
from goVolt.settings import AUTH_DB
from goVolt.settings import FIREBASE_DB
from firebase_admin import auth, exceptions
from .serializers import UserSerializer

def logout(request) :
    try:
        AUTH_DB.current_user = None
        return 200
    except Exception as e:
        return e
    
def get_auth_user(email, password):
    
    try:
        AUTH_DB.sign_in_with_email_and_password(email, password)

        #user = FIREBASE_DB.collection('users').document(firebase_uid).get()

        return 200
    except Exception as e:
        return e
        

def store_user(email, password, phone):
    # Crea una cuenta de usuario en Firebase Authentication
    try:
        user = auth.create_user(
            email=email,
            password=password,
            phone_number=phone,
        )

        # insertar usuarios en la bbdd
        collection_name = 'users'
        user_data = {
            'first_name': None,
            'last_name': None,
            'photo_url': None,
            'phone': phone,
            'email': email,
            'firebase_uid': user.uid
        }

        collection_ref = FIREBASE_DB.collection(collection_name)
        # Crea un documento con el ID del usuario (UID) y almacena los datos
        collection_ref.document(user.uid).set(user_data)

        return 200
    except Exception as e:
        return e

def get_see_my_profile():

    # Obten el token de autenticación de la solicitud
    firebase_uid = AUTH_DB.current_user["localId"]

    user_ref = FIREBASE_DB.collection('users').document(firebase_uid)

    res = user_ref.get()

    data = {}
    data['first_name'] =  res.get('first_name')
    data['last_name'] =  res.get('last_name')
    data['photo_url']= res.get('photo_url')
    data['phone']= res.get('phone')
    data['email']= res.get('email')

    serializer = UserSerializer(data=data)
    
    if serializer.is_valid():
        return serializer.data
    else:
        raise serializer.ValidationError(serializer.errors)
    
def edit_user(first_name, last_name, phone, photo_url):
    # Verifica si el usuario está autenticado
    if not AUTH_DB.current_user:
        return 401  # Código de estado HTTP para no autorizado

    # Crea una cuenta de usuario en Firebase Authentication
    try:

        # Obten el token del usuario registrado
        firebase_uid = AUTH_DB.current_user["localId"]

        user_ref = FIREBASE_DB.collection('users').document(firebase_uid)

        user_ref.update({
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'photo_url': photo_url,
        })

        return 200
    except Exception as e:
        return e