from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from api.chats.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})