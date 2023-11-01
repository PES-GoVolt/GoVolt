from channels.routing import URLRouter
from django.urls import include,path

from api.chats.routing import chats_websocket_patterns

websocket_patterns = [
    path('ws/<int:user_id>/chats/',URLRouter(chats_websocket_patterns)),
]