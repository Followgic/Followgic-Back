from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # Nombre del usuario actual
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Creo una sala con el nombre del usuario actual
        self.room_group_name = self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    # broadcast Notification; Individual + community
        def broadcast_notification_message(self, event):
            message = event['message']
            self.send(text_data=json.dumps({'message': message
                                            }))
