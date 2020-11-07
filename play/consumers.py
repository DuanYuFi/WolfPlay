from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync
import play.game
from play.chats import addMessageToDatabase


class ChatConsumer(WebsocketConsumer):

    def receive(self, text_data = None):
        '''
            text_data's structure:
            text_data {
                content: processedData string,
                user: username string,
                type: MessageType string,
            }
        '''
        # print(self.room_group_name)
        data = json.loads(text_data)
        addMessageToDatabase(data, self.roomname)
        if data['type'] == 'normal-content' or data['type'] == 'newLogin' or data['type'] == 'Logout':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, 
                {
                'type': 'sendMessage', 
                'message': data
            })

        elif data['type'] == 'game-control':
            play.game.processData(data['data'], self.roomname)
        
    
    def sendMessage(self, event):
        self.send(json.dumps(event['message']))

    def connect(self):

        self.roomname = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.roomname

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        self.close()