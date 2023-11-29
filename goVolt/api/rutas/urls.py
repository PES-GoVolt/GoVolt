from django.urls import path
from .views import AllRoutesView,ParticipantView,RouteByIdView,MyRoutesView

urlpatterns = [
    # gestión general rutas / creación
    path('', AllRoutesView.as_view(), name='all-routes'),

    # gestión rutas en las que soy participante
    path('my_routes', ParticipantView.as_view(), name='my-routes'),

    # gestión ruta especifica a partir del id
    path('<str:id>', RouteByIdView.as_view(), name='route-by-id'),

    # gestión de las rutas creadas por mi
    path('my', MyRoutesView.as_view(), name='my-routes'),
]