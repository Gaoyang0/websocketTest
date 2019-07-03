# -*- coding:utf-8 -*-
# Author:DaoYang

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user']
        self.room_group_name = 'chat_%s' % self.room_name

        print(self.room_name)
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # 接受WebSocket连接
        await self.accept()

    # 断开连接(组)
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        flag = text_data_json['flag']

        if flag == 'upload':
            # Send message to room group
            print("send to client!")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'get_res',
                    'message': message
                }
            )
        elif flag == 'res':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_res',
                    'message': message
                }
            )


    async def get_res(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'flag': "getRes",
            'message': message
        }))


    async def send_res(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'flag': "res",
            'message': message
        }))
