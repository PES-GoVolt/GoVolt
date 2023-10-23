from django.urls import path
from .views import BikeStationsDatabaseApiView,BikeStationsApiView

urlpatterns = [
    path('database',BikeStationsDatabaseApiView.as_view(),name='bikestations-database'),
    path('all',BikeStationsApiView.as_view(),name='bikestations-loc')
]