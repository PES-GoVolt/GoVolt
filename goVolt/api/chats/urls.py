from django.urls import path
from .views import ChatsAPIView
urlpatterns = [
    path('',ChatsAPIView.as_view(),name='chats-view'),
]