from django.urls import path
from .views import AllRoutesView,ParticipantView,RouteByIdView,MyRoutesView

urlpatterns = [
    # gestión general rutas / creación
    path('', AllRoutesView.as_view(), name='all-routes'),

    # gestión rutas en las que soy participante
        # get - todas las rutas en las que participo
    path('/my_current_routes', ParticipantView.as_view(), name='my-current-routes'),

    # gestión de las rutas creadas por mi
        # get - 
        # post -
        # delete - 
    path('/my_routes', MyRoutesView.as_view(), name='my-routes'),

    # gestión ruta especifica a partir del id
    path('/<str:id>', RouteByIdView.as_view(), name='route-by-id'),

    
]