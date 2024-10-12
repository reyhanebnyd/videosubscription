import json  
from channels.generic.websocket import AsyncWebsocketConsumer  

class MovieConsumer(AsyncWebsocketConsumer):  

    async def connect(self):  
        self.movie_id = self.scope['url_route']['kwargs']['movie_id']  
        self.room_group_name = f'movie_{self.movie_id}'  

        
        await self.channel_layer.group_add(  
            self.room_group_name,  
            self.channel_name  
        )  

        await self.accept()  

    async def disconnect(self, close_code):  
 
        await self.channel_layer.group_discard(  
            self.room_group_name,  
            self.channel_name  
        )  

    async def receive(self, text_data):  
        data = json.loads(text_data)  
         

    async def send_update(self, event):  
       
        await self.send(text_data=json.dumps(event))