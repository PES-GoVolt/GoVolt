from django.urls import path
from .views import CrearRutaViajeView, GetMisRutasView, GetAllRutasView, GetRutaByIdView, EditarRutaViajeView

urlpatterns = [
    #crear una ruta
    path('create/', CrearRutaViajeView.as_view(), name='create-route'),
    #obtener todos los viajes/rutas que he creado
    path('my/', GetMisRutasView.as_view(), name='get-my-routes'),
    # obtener una ruta especifica a partir del id
    path('<str:id>/', GetRutaByIdView.as_view(), name='get-route-by-id'),
    # editar info rutas
    path('edit/<str:id>/', EditarRutaViajeView.as_view(), name='edit-route'),
    # listar todas las rutas
    path('', GetAllRutasView.as_view(), name='get-all-routes'),
    # añadir participantes a rutas
    # obtener rutas en las que soy participante
]