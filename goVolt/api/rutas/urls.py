from django.urls import path
from .views import CrearRutaViajeView, GetMisRutasView, GetAllRutasView

urlpatterns = [
    #crear una ruta
    path('create-route/', CrearRutaViajeView.as_view(), name='create-route'),
    #obtener todos los viajes/rutas que he creado
    path('get-my-routes/', GetMisRutasView.as_view(), name='get-my-routes'),
    # obtener una ruta especifica a partir del id
    # editar info rutas
    # listar todas las rutas
    path('get-all-routes/', GetAllRutasView.as_view(), name='get-all-routes'),
    # añadir participantes a rutas
    # obtener rutas en las que soy participante
]