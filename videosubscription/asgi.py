"""
ASGI config for videosubscription project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter  
from channels.auth import AuthMiddlewareStack  
from yourapp.consumers import MovieConsumer  # Adjust as needed  
from django.urls import path  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')  

application = ProtocolTypeRouter({  
    "http": get_asgi_application(),  
    "websocket": AuthMiddlewareStack(  
        URLRouter([  
            path("ws/movies/<int:movie_id>/", MovieConsumer.as_asgi()),  
        ])  
    ),  
})