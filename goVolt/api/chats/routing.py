from channels.routing import URLRouter
from django.urls import include,path
from .consumers import Consumer
chats_websocket_patterns = [
    path('messages/', Consumer.as_asgi())
]