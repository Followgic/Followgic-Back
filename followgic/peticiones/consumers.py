import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    room_name = None
    room_group_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'peticion_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channels_name
        )
        await self.accept()

    async def disconnect(self):
        if self.room_group_name and self.channel_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            ) 

    async def receive(self, text_data= None, bytes_data=None):
        event = json.loads(text_data)
        message = event['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'peticion',
                'username': self.scope['user'].username.name,
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))