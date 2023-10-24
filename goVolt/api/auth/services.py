
from firebase_admin import firestore
import pandas as pd
from sodapy import Socrata
from rest_framework import serializers
from goVolt.settings import AUTH_DB
from goVolt.settings import FIREBASE_DB
from firebase_admin import auth, exceptions

def get_auth_user(email, password):
    try:
        AUTH_DB.sign_in_with_email_and_password(email, password)
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