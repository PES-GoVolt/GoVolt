from firebase_admin import firestore
import pandas as pd
from sodapy import Socrata
from rest_framework import serializers
from goVolt.settings import AUTH_DB
from goVolt.settings import FIREBASE_DB
from firebase_admin import auth, exceptions
from .serializers import RutaViajeSerializer
import json
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.users.models import CustomUser

def store_ruta(data):

    try:   

        creador_id = AUTH_DB.current_user["localId"]
        #creador_id = "cNtxKjlvPTM6TE6aaTC6mjl1hj12"

        data['creador'] = creador_id

        serializer = RutaViajeSerializer(data=data)

        if serializer.is_valid():
            collection_ref = FIREBASE_DB.collection('rutas')
            new_ruta = collection_ref.add(serializer.data)

            return Response({'message': new_ruta[1].id},status=200)
        else:
            raise ValidationError(serializer.errors)
        
    except Exception as e:
        return Response({'message': str(e)},status=400)

def get_mis_rutas():
    creador_id = AUTH_DB.current_user["localId"]
    #creador_id = "cNtxKjlvPTM6TE6aaTC6mjl1hj12"

    rutas_ref = FIREBASE_DB.collection('rutas')
    rutas = rutas_ref.where('creador', '==', creador_id).get()

    # Itera sobre los resultados para obtener los datos de las rutas encontradas
    rutas_encontradas = []
    for resultado in rutas:
        datos_ruta = resultado.to_dict()
        # Agrega el identificador del documento a los datos de la ruta
        datos_ruta['id'] = resultado.id
        rutas_encontradas.append(datos_ruta)
    
    return rutas_encontradas

def get_all_rutas():

    rutas_ref = FIREBASE_DB.collection('rutas')
    rutas = rutas_ref.get()

    # Itera sobre los resultados para obtener los datos de las rutas encontradas
    rutas_encontradas = []
    for resultado in rutas:
        datos_ruta = resultado.to_dict()
        # Agrega el identificador del documento a los datos de la ruta
        datos_ruta['id'] = resultado.id
        rutas_encontradas.append(datos_ruta)
    
    return rutas_encontradas

