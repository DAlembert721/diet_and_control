import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework import status

from accounts.models import Profile, User
from communications.models import Chat, Message


class ChatConsumer(WebsocketConsumer):

    def init_chat(self, data):
        username = data['username']
        chat_id = data['chat_id']
        # user = User.objects.get(email=username)
        profile = Profile.objects.get(user__email=username)
        chat = Chat.objects.filter(id=chat_id)

        if not profile or not chat:
            raise Exception("User or Room don't founded", status.HTTP_404_NOT_FOUND)

        content = {
            'command': 'init_chat'
        }
        if not profile:
            content['error'] = 'Unable to get or create User with username: ' + username
            self.send_message(content)
        content['success'] = 'Chatting in with success with username: ' + username
        content['chat_id'] = chat_id
        self.send_message(content)

    def fetch_messages(self, data):
        messages = Message.last_50_message(data['chat'])
        content = {
            'command': 'message',
            'messages': self.messages_to_json(messages),
            'chat_id': data['chat']
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        text = data['text']
        chat_id = data['chat']
        user = User.objects.get(email=author)
        # print(user)
        author_profile = Profile.objects.get(user_id=user.id)
        # print(author_profile)
        chat = Chat.objects.get(id=chat_id)
        if not chat:
            raise Exception('Chat did not founded', status.HTTP_404_NOT_FOUND)
        message = Message.objects.create(author=author_profile, content=text, chat=chat)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message),
            'chat_id': chat_id
        }
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        # print(list(messages))
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    @staticmethod
    def message_to_json(message):

        return {
            'id': str(message.id),
            'author': message.author.user.email,
            'content': message.content,
            'created_at': str(message.created_at),
            'chat_id': str(message.chat.id)
        }

    commands = {
        'init_chat': init_chat,
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_code']
        self.chat_group_name = 'chat_' + self.chat_name

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
