from django.urls import path
from .views import CrearRutaViajeView, GetMisRutasView, GetAllRutasView, GetRutaByIdView, EditarRutaViajeView, AddParticipantRutaViajeView, GetRutasParticipadasView, RemoveParticipantRutaViajeView

urlpatterns = [
    # listar todas las rutas
    path('', GetAllRutasView.as_view(), name='get-all-routes'),
    #crear una ruta
    path('create/', CrearRutaViajeView.as_view(), name='create-route'),
    #obtener todos los viajes/rutas que he creado
    path('my/', GetMisRutasView.as_view(), name='get-my-routes'),
    # obtener rutas en las que soy participante
    path('participant_route/', GetRutasParticipadasView.as_view(), name='get-route-participant'),
    # obtener una ruta especifica a partir del id
    path('<str:id>/', GetRutaByIdView.as_view(), name='get-route-by-id'),
    # editar info rutas
    path('edit/<str:id>/', EditarRutaViajeView.as_view(), name='edit-route'),
    # añadir participante a ruta
    path('add_participant/<str:ruta_id>/<str:participant_id>/', AddParticipantRutaViajeView.as_view(), name='add-participant-route'),
    # eliminar participante de ruta
    path('remove_participant/<str:ruta_id>/<str:participant_id>/', RemoveParticipantRutaViajeView.as_view(), name='remove-participant-route'),
]