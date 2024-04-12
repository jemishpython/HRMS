# routing.py
from django.urls import path

from .consumers import ChatConsumer, GroupChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),
    path('ws/group-chat/<room_name>/', GroupChatConsumer.as_asgi()),
]
