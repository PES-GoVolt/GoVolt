from django.urls import path
from .views import ChatsAPIView
from .views import room
urlpatterns = [
    path('',ChatsAPIView.as_view(),name='chats-view'),
    path('templates/<str:room_name>',room,name='template_test')
]