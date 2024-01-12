from django.urls import path

from .views import MessagesAPIView, ChatsAPIView

urlpatterns = [
    path('',MessagesAPIView.as_view(),name='messages-view'),
    path('chats/',ChatsAPIView.as_view(),name='chats-view')
]