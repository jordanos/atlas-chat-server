import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa

django.setup()

import ws.routing  # noqa
from authentication.channels_auth import CustomTokenAuthMiddleware  # noqa
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa
from django.core.asgi import get_asgi_application  # noqa

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": CustomTokenAuthMiddleware(
            URLRouter(ws.routing.websocket_urlpatterns)
        ),
    }
)
