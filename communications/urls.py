from django.urls import path

from communications.views import list_chats_by_user, chat_detail

urlpatterns = [
    path('profiles/<int:user_id>/chats/', list_chats_by_user, name='list_chats_by_user'),
    path('profiles/<int:user_id>/receivers/<int:receiver_id>/chats/', chat_detail, name='chat_detail'),
]