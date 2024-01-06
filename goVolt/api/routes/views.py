from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RutaViaje
from api.routes.services import store_ruta, get_mis_rutas, get_all_rutas, get_ruta_by_id, edit_ruta, add_participant, \
    get_routes_participadas, remove_participant, add_request_participant, remove_request_participant, remove_route
import json

from rest_framework.permissions import IsAuthenticated
from api.users.authentication import FirebaseAuthentication

class AllRoutesView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    # devuelvo todas las rutas - que no he creado yo ni soy participante
    def get(self, request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        return Response({'rutas': get_all_rutas(firebase_token)}, status=status.HTTP_200_OK)

    def post(self, request):

            firebase_token = request.headers.get("Authorization", "").split(" ")[1]
            
            result = store_ruta(firebase_token, request.data)

            if (result.status_code != 200):
                code = result.status_code

                if code == 400:
                    st = status.HTTP_400_BAD_REQUEST
                elif code == 401:
                    st = status.HTTP_401_UNAUTHORIZED
                elif code == 403:
                    st = status.HTTP_403_FORBIDDEN
                elif code == 404:
                    st = status.HTTP_404_NOT_FOUND
                elif code == 500:
                    st = status.HTTP_500_INTERNAL_SERVER_ERROR

                return Response({"message": result.data.get('message')}, status=st)

            else:
                # Si result no es una excepción, es el resultado exitoso
                return Response({'message': result.data.get('message')}, status=status.HTTP_200_OK)
    
    def delete(self, request):

        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        
        data = request.data
        ruta_id = data['route_id']
        
        # remove the route
        result = remove_route(firebase_token, ruta_id)

        if (result.status_code != 200):
            # Verificar si result es una excepción
            code = result.status_code

            if code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": result.data.get('message')}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message': 'Successful Remove Route'}, status=status.HTTP_200_OK)

class ParticipantView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def get(self, request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]

        rutas = get_routes_participadas(firebase_token)
        if rutas is not None:
            return Response({"rutas": rutas}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Routes not found"}, status=status.HTTP_404_NOT_FOUND)

class RouteByIdView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def get(self, request, id):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]

        ruta = get_ruta_by_id(firebase_token, id)
        if ruta is not None:
            return Response(ruta, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Ruta not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]

        data = json.loads(request.body)

        ubicacion_inicial = data.get('ubicacion_inicial')
        ubicacion_final = data.get('ubicacion_final')
        precio = data.get('precio')
        num_plazas = data.get('num_plazas')
        fecha = data.get('fecha')
        creador = data.get('creador')

        result = edit_ruta(firebase_token, id, ubicacion_inicial, ubicacion_final, precio, num_plazas, fecha, creador)

        if (result.status_code != 200):
            # Verificar si result es una excepción
            code = result.status_code

            if code == 200:
                st = status.HTTP_200_OK
            elif code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": result.data.get('message')}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message':'Successful Edit'},status=status.HTTP_200_OK)

class MyRoutesView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    # listar rutas que he creado yo
    def get(self, request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        return Response({'rutas': get_mis_rutas(firebase_token)}, status=status.HTTP_200_OK)
    
    # añadir participante a ruta
    def post(self, request):

        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        
        data = request.data
        ruta_id = data['route_id']
        participant_id = data['participant_id']

        # Get the route instance
        result = add_participant(firebase_token, ruta_id, participant_id)

        if (result.status_code != 200):
            # Verificar si result es una excepción
            code = result.status_code

            if code == 200:
                st = status.HTTP_200_OK
            elif code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": result.data.get('message')}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message': 'Successful Edit'}, status=status.HTTP_200_OK)
    
    # eliminar participante de ruta
    def delete(self, request):

        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        
        data = request.data
        ruta_id = data['route_id']
        participant_id = data['participant_id']
        participant_name = data['participant_name']
        
        # Get the route instance
        result = remove_participant(firebase_token, ruta_id, participant_id, participant_name)

        if (result.status_code != 200):
            # Verificar si result es una excepción
            code = result.status_code

            if code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": result.data.get('message')}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message': 'Successful Remove Participant'}, status=status.HTTP_200_OK)

class RequestsView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    # usuario pide ser participante
    def post(self, request):

        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        
        data = request.data
        ruta_id = data['route_id']

        # Get the route instance
        result = add_request_participant(firebase_token, ruta_id)

        if (result.status_code != 200):
            # Verificar si result es una excepción
            code = result.status_code

            if code == 200:
                st = status.HTTP_200_OK
            elif code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": result.data.get('message')}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message':'Successful Edit Request'},status=status.HTTP_200_OK)

    def delete(self, request):

        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        data = request.data
        ruta_id = data['route_id']
        participant_id = data['participant_id']

        # Get the route instance
        result = remove_request_participant(firebase_token, ruta_id, participant_id)

        if (result.status_code != 200):
            # Verificar si result es una excepción
            code = result.status_code

            if code == 200:
                st = status.HTTP_200_OK
            elif code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": result.data.get('message')}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message':'Successful Deleted Request'},status=status.HTTP_200_OK)