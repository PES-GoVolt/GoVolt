from django.urls import path
from .views import CrearRutaViajeView, GetMisRutasView

urlpatterns = [
    path('create-route/', CrearRutaViajeView.as_view(), name='create-route'),
    path('get-my-routes/', GetMisRutasView.as_view(), name='get-my-routes'),
]