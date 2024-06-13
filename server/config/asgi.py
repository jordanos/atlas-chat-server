import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

import ws.routing
from authentication.channels_auth import CustomTokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": CustomTokenAuthMiddleware(
            URLRouter(ws.routing.websocket_urlpatterns)
        ),
    }
)
