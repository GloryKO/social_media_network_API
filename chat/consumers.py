import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.room_name= self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        #join room group 
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,self.channel_name
        )

        self.accept()

    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,self.channel_name
        )

    def recieve(self,text_data):
        
        text_data_json=json.loads(text_data)
        message = text_data_json['message']
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'chat.message',
                'message':message
            }
        )
    
    def chat_message(self,event):
        #send message to the websocket
        message = event['message']
        self.send(text_data=json.dumps({'message':message}))