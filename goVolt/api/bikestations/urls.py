from django.urls import path
from .views import BikeStationsDatabaseApiView

urlpatterns = [
    path('database',BikeStationsDatabaseApiView.as_view(),name='bikestations-database')
]