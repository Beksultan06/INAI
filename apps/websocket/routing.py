from django.urls import path

from apps.websocket.consumer import ChatConsumer
from apps.websocket.consumer_status import OrderTrackingConsumer


websocket_urlpatterns = [
    path('ws/orders/<str:order_id>/', OrderTrackingConsumer.as_asgi()),
    path('ws/chat/<str:order_id>/', ChatConsumer.as_asgi()),
]
