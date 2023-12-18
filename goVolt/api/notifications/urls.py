from django.urls import path
from .views import NotificationsAPIView
urlpatterns = [
    path('',NotificationsAPIView.as_view(),name='notifications-view'),
]