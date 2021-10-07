from django.conf.urls import url

from communications.chat_consumer import ChatConsumer

channel_routing = [
    url(r'^ws/chat/(?P<chat_code>\w+)$', ChatConsumer.as_asgi())
]