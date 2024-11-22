import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'chat_{self.order_id}'

        # Подключение к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключение от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        message = data['message']

        # Сохранение сообщения в базе данных
        await self.save_message(sender_id, receiver_id, self.order_id, message)

        # Отправка сообщения в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message': message,
            }
        )

    async def chat_message(self, event):
        # Отправка сообщения клиенту WebSocket
        await self.send(text_data=json.dumps({
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
            'message': event['message'],
        }))

    @sync_to_async
    def save_message(self, sender_id, receiver_id, order_id, message):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            order_id=order_id,
            message=message
        )
