import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from django.core.asgi import get_asgi_application
import tiempo_real.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'followgic.settings')
django_asgi_app = get_asgi_application()
django.setup()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  # Just HTTP for now. (We can add other protocols later.)
  "websocket": AuthMiddlewareStack(
        URLRouter(
            tiempo_real.routing.websocket_urlpatterns
        )
    ),
})
