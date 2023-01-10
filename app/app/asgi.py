"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this files, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notification.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(notification.routing.websocket_urlpatterns))
        ),
        # AuthMiddlewareStack(URLRouter(notification.routing.websocket_urlpatterns)
    }
)
