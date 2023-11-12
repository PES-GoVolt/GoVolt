from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RutaViaje
from api.rutas.services import store_ruta,get_mis_rutas, get_all_rutas, get_ruta_by_id, edit_ruta
import json

# Create your views here.
class CrearRutaViajeView(APIView):
    def post(self, request, *args, **kwargs):

        result = store_ruta(request.data)

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
            return Response({'message':result.data.get('message')},status=status.HTTP_200_OK)

class GetMisRutasView(APIView):
    def get(self,request):
        return Response({'rutas':get_mis_rutas()},status=status.HTTP_200_OK)

class GetAllRutasView(APIView):
    def get(self,request):
        return Response({'rutas':get_all_rutas()},status=status.HTTP_200_OK)
    
class GetRutaByIdView(APIView):
    def get(self,request, id):
        ruta = get_ruta_by_id(id)
        if ruta is not None:
            return Response(ruta, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Ruta not found"}, status=status.HTTP_404_NOT_FOUND)

class EditarRutaViajeView(APIView):
    def post(seld, request, id):
        data = json.loads(request.body)

        ubicacion_inicial = data.get('ubicacion_inicial')
        ubicacion_final = data.get('ubicacion_final')
        precio = data.get('precio')
        num_plazas = data.get('num_plazas')
        fecha = data.get('fecha')
        creador = data.get('creador')

        result = edit_ruta(id, ubicacion_inicial, ubicacion_final, precio, num_plazas, fecha, creador)

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