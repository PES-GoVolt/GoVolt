from django.urls import path

from .views import ChargerLocationApiView, ChargerDataBaseApiView, ChargerApiView, NearestChargerApiView

urlpatterns = [
    path('all',ChargerLocationApiView.as_view(),name='chargers-loc'),
    path('database',ChargerDataBaseApiView.as_view(),name='chargers-database'),
    path('nearest',NearestChargerApiView.as_view(),name='chargers-nearest'),
    path('<str:id>',ChargerApiView.as_view(),name='charger-detail')
]