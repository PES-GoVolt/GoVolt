from django.urls import path

from .views import AllRoutesView, ParticipantView, RouteByIdView, MyRoutesView, RequestsView

urlpatterns = [
    # gestión general rutas / creación
        # get - obtengo todas las rutsa menos las que he creado y en las que participo
        # post - creo una ruta
        # delete - elimino una ruta
    path('', AllRoutesView.as_view(), name='all-routes'),

    # gestión rutas en las que soy participante
        # get - todas las rutas en las que participo
    path('/my_current_routes', ParticipantView.as_view(), name='my-current-routes'),

    # gestión de las rutas creadas por mi
        # get - todas las rutas que he creado
        # post - añado participante a ruta
        # delete - elimino participante de ruta
    path('/my_routes', MyRoutesView.as_view(), name='my-routes'),

    # usuario pide ser participante
    path('/requests', RequestsView.as_view(), name='requests-participant'),

    # gestión ruta especifica a partir del id
        # get - obtengo la info de una ruta con id = ID
        # post - edito una ruta con id = ID
    path('/<str:id>', RouteByIdView.as_view(), name='route-by-id'),
]