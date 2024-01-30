# your_project/routing.py

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import social_media.routing  

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            social_media.routing.websocket_urlpatterns
        )
    ),
})
