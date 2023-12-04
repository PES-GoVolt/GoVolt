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

from google.cloud.firestore_v1.base_query import FieldFilter

def store_ruta(firebase_token, data):
    try:

        decoded_token = auth.verify_id_token(firebase_token)
        creador_id = decoded_token['uid']

        users_ref = FIREBASE_DB.collection('users')
        user = users_ref.where('firebase_uid', '==', creador_id).get()[0].to_dict()

        data['creador'] = creador_id
        data['participantes'] = None
        data['username'] = user['username']

        serializer = RutaViajeSerializer(data=data)

        if serializer.is_valid():
            collection_ref = FIREBASE_DB.collection('rutas')
            new_ruta = collection_ref.add(serializer.data)

            return Response({'message': new_ruta[1].id}, status=200)
        else:
            raise ValidationError(serializer.errors)

    except Exception as e:
        return Response({'message': str(e)}, status=400)


def get_mis_rutas(firebase_token):

    decoded_token = auth.verify_id_token(firebase_token)
    creador_id = decoded_token['uid']

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


def get_all_rutas(firebase_token):

    decoded_token = auth.verify_id_token(firebase_token)
    logged_id = decoded_token['uid']
    #logged_id = "abc"
    
    rutas_no_creadas_ref = FIREBASE_DB.collection('rutas').where('creador', '!=', logged_id)
    rutas_no_creadas = rutas_no_creadas_ref.get()

    rutas_participadas_ref = FIREBASE_DB.collection('rutas').where('participantes', 'array_contains', logged_id)
    rutas_participadas = rutas_participadas_ref.get()

    rutas = [ruta for ruta in rutas_no_creadas if ruta.id not in [ruta.id for ruta in rutas_participadas]]

    # Itera sobre los resultados para obtener los datos de las rutas encontradas
    rutas_encontradas = []
    for resultado in rutas:
        datos_ruta = resultado.to_dict()
        # Agrega el identificador del documento a los datos de la ruta
        datos_ruta['id'] = resultado.id
        rutas_encontradas.append(datos_ruta)

    return rutas_encontradas


def get_ruta_by_id(firebase_token, id):
    decoded_token = auth.verify_id_token(firebase_token)
    logged_id = decoded_token['uid']
    
    doc_ref = FIREBASE_DB.collection('rutas').document(id)

    res = doc_ref.get()

    data = {}
    data['id'] = id
    data['ubicacion_inicial'] = res.get('ubicacion_inicial')
    data['ubicacion_final'] = res.get('ubicacion_final')
    data['precio'] = res.get('precio')
    data['num_plazas'] = res.get('num_plazas')
    data['fecha'] = res.get('fecha')
    data['creador'] = res.get('creador')
    data['creador_email']= res.get('creador_email')
    # data['participantes']= res.get('participantes')

    serializer = RutaViajeSerializer(data=data)
    if serializer.is_valid():
        return serializer.data
    else:
        raise serializers.ValidationError(serializer.errors)


def edit_ruta(firebase_token, id, ubicacion_inicial, ubicacion_final, precio, num_plazas, fecha, creador):
    try:
        
        decoded_token = auth.verify_id_token(firebase_token)
        firebase_uid = decoded_token['uid']

        ruta_ref = FIREBASE_DB.collection('rutas').document(id)

        # comprueba que el usuario que edita la ruta sea el creador
        if (firebase_uid == creador):
            ruta_ref.update({
                'ubicacion_inicial': ubicacion_inicial,
                'ubicacion_final': ubicacion_final,
                'precio': precio,
                'num_plazas': num_plazas,
                'fecha': fecha
            })

            return Response({'message': "OK"}, status=200)
        else:
            return Response({'message': "USER UNAUTHORIZED"}, status=401)

    except Exception as e:
        error_message = e.args[1]
        error_data = json.loads(error_message)

        code = error_data['error']['code']
        msg = error_data['error']['message']

        return Response({'message': msg}, status=code)


def add_participant(firebase_token, ruta_id, participant_id):
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        logged_user = decoded_token['uid']

        ruta_ref = FIREBASE_DB.collection('rutas').document(ruta_id)
        res = ruta_ref.get().to_dict()

        creador_ruta = res.get("creador")

        # si el que añade no es el creador ni el participante => error
        if (logged_user == creador_ruta):
            # comprobar que num_plazas > count(participantes)
            participantes = res.get("participantes")

            if (participantes == None):
                participantes = []

            if participant_id not in participantes:
                if (res.get("num_plazas") > len(participantes)):
                    participantes.append(participant_id)
                    ruta_ref.update({"participantes": participantes})

                    query = FIREBASE_DB.collection('requests_participants').where(filter=FieldFilter('user_id', '==', logged_user)).where(filter=FieldFilter('ruta_id', '==', ruta_id))
                    requests = query.get()

                    # Verifica si hay resultados
                    if requests:
                        requests[0].reference.delete()

                    # si ya estan todas las plazas llenas
                    if (res.get("num_plazas") == (len(participantes))):
                        query = FIREBASE_DB.collection('requests_participants').where(filter=FieldFilter('ruta_id', '==', ruta_id))
                        requests = query.get()

                        # Verifica si hay request existentes
                        if requests:
                            # Elimina cada request encontrada
                            for request in requests:
                                request.reference.delete()

                    return Response({'message': "OK"}, status=200)

                else:
                    return Response({'message': "TOO MANY PARTICIPANTS"}, status=500)
            else:
                return Response({'message': "PARTICIPANT ALREADY EXIST"}, status=500)
        else:
            return Response({'message': "USER UNAUTHORIZED"}, status=401)

    except Exception as e:
        error_message = e.args[1]
        error_data = json.loads(error_message)

        code = error_data['error']['code']
        msg = error_data['error']['message']

        return Response({'message': msg}, status=code)

def get_routes_participadas(firebase_token):
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        participant_id = decoded_token['uid']

        # Query Firestore for routes where the participant is in the participantes array
        routes_ref = FIREBASE_DB.collection('rutas')
        query = routes_ref.where('participantes', 'array_contains', participant_id)
        routes = query.stream()

        routes_found = []
        for route in routes:
            route_data = route.to_dict()
            route_data['id'] = route.id
            routes_found.append(route_data)

        return routes_found

    except Exception as e:
        print(str(e))
        return []

def remove_participant(firebase_token, ruta_id, participant_id):
    try:

        decoded_token = auth.verify_id_token(firebase_token)
        logged_user = decoded_token['uid']

        ruta_ref = FIREBASE_DB.collection('rutas').document(ruta_id)
        res = ruta_ref.get()

        creador_ruta = res.get("creador")
        participante = participant_id

        # si el que añade no es el creador ni el participante => error
        if (logged_user == creador_ruta or logged_user == participante):

            participantes = res.get("participantes")

            if participant_id in participantes:
                participantes.remove(participant_id)
                ruta_ref.update({"participantes": participantes})

                return Response({'message': "OK"}, status=200)
            else:
                return Response({'message': "PARTICIPANT NOT EXIST"}, status=500)
        else:
            return Response({'message': "USER UNAUTHORIZED"}, status=401)

    except Exception as e:
        error_message = e.args[1]
        error_data = json.loads(error_message)

        code = error_data['error']['code']
        msg = error_data['error']['message']

        return Response({'message': msg}, status=code)

def add_request_participant(firebase_token, ruta_id):
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        logged_user = decoded_token['uid']

        ruta_ref = FIREBASE_DB.collection('rutas').document(ruta_id)
        res = ruta_ref.get().to_dict()
        
        # comprobar que num_plazas > count(participantes)
        participantes = res.get("participantes") or []

        if logged_user not in participantes:
            if (res.get("num_plazas") > len(participantes)):
                # Realiza la consulta en la colección requests_participants
                query = FIREBASE_DB.collection('requests_participants').where(filter=FieldFilter('user_id', '==', logged_user)).where(filter=FieldFilter('ruta_id', '==', ruta_id))
                request = query.get()

                #Verifica si hay resultados
                if not request:
                    # No hay resultados, inserta un nuevo documento
                    new_request = {
                        'user_id': logged_user,
                        'ruta_id': ruta_id,
                    }
                    FIREBASE_DB.collection('requests_participants').add(new_request)
                    return Response({'message': "OK"},status=200)
                else:
                    # Ya existen documentos con los valores proporcionados
                    return Response({'message': "THE REQUEST ALREADY EXIST"}, status=500)

            else:
                return Response({'message': "TOO MANY PARTICIPANTS"}, status=500)
        else:
            return Response({'message': "PARTICIPANT ALREADY EXIST"}, status=500)

    except Exception as e:
        error_message = e.args[1]
        error_data = json.loads(error_message)

        code = error_data['error']['code']
        msg = error_data['error']['message']

        return Response({'message': msg},status=code)

def remove_request_participant(firebase_token, ruta_id, participant_id):
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        logged_user = decoded_token['uid']
        
        ruta_ref = FIREBASE_DB.collection('rutas').document(ruta_id)
        res = ruta_ref.get().to_dict()
        creador_ruta = res.get("creador")

        if(logged_user == creador_ruta or logged_user == participant_id):

                # Realiza la consulta en la colección requests_participants
                query = FIREBASE_DB.collection('requests_participants').where(filter=FieldFilter('user_id', '==', participant_id)).where(filter=FieldFilter('ruta_id', '==', ruta_id))
                requests = query.get()

                #Verifica si hay resultados y lo elimina
                if requests:
                    requests[0].reference.delete()
                    return Response({'message': "OK"},status=200)
                else:
                    # Ya existen documentos con los valores proporcionados
                    return Response({'message': "THE REQUEST DOES NOT EXIST"}, status=500)

        else:
            return Response({'message': "USER UNAUTHORIZED"}, status=401)

    except Exception as e:
        error_message = e.args[1]
        error_data = json.loads(error_message)

        code = error_data['error']['code']
        msg = error_data['error']['message']

        return Response({'message': msg},status=code)