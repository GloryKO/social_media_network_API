# chat/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import ChatConsumer

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/chat/<int:chat_room_id>/", ChatConsumer.as_asgi()),
                ]
            )
        ),
    }
)
