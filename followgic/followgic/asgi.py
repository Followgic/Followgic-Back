import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import peticiones.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'followgic.settings')


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  # Just HTTP for now. (We can add other protocols later.)
  "websocket": AuthMiddlewareStack(
        URLRouter(
            peticiones.routing.websocket_urlpatterns
        )
    ),
})
