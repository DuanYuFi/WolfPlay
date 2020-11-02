from django.urls import path
from django.conf.urls import url
from play.consumers import ChatConsumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer)
]
