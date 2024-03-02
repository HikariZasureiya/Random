import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import messaging
from django.contrib.auth.models import User
# from lsystem.models import pim

online_users = []

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test'
        user = self.scope['user']

        # userprofile = await sync_to_async(pim.objects.get)(username=user.username)

        if user.is_authenticated:
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            online_users.append(user.username)



            await self.accept()
            print(online_users)
            # if online_users.count(user.username)<=1:
            await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'user_joined',
                        'username': user.username,
                        'online_list':list(set(online_users)),
                    }
                )
            # await self.send(text_data=json.dumps({
            #     'type': 'connection',
            #     'users_online': list(online_users)
            # }))

        else:
            await self.close(code=4401)

    async def receive(self, text_data):
        text_json_data = json.loads(text_data)
        the_message = text_json_data['message']
        username = self.scope['user'].username

       
        




        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': the_message,
                'username':username,
            }
        )


    async def chat_message(self, event):
        a_message = event['message']
        sender_username = event.get('username')
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': a_message,
            'username': sender_username

        }))

    async def user_joined(self, event):

        print("works")
        user = self.scope['user']
        # userprofile = await sync_to_async(pim.objects.get)(username=user.username)
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'username': event['username'],
            'online_list':list(set(online_users)),
            # 'userpfp':userprofile.profilepic,
        }))


    async def disconnect(self, close_code):
        

        user = self.scope['user']
        online_users.remove(user.username)

        if online_users.count(user.username)==0:

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'offline',
                    'username':user.username,        
                    'online_list':list(set(online_users)),
                }

            )

    async def offline(self, event):

        user = self.scope['user']
        
        await self.send(text_data=json.dumps({
            'type': 'offline',
            'username': event['username'],
            'online_list':list(set(online_users)),
        }))
