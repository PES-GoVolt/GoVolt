from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RutaViaje
from api.rutas.services import store_ruta,get_mis_rutas, get_all_rutas

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