from django.urls import path
from .views import ChargerLocationApiView

urlpatterns = [
    path('',ChargerLocationApiView.as_view(),name='charger-loc')
]