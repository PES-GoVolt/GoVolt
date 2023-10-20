from django.urls import path
from .views import ChargerLocationApiView,ChargerDataBaseApiView

urlpatterns = [
    path('',ChargerLocationApiView.as_view(),name='chargers-loc'),
    path('database',ChargerDataBaseApiView.as_view(),name='chargers-database')
]