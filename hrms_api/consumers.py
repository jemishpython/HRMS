# consumers.py
import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from hrms_api.models import GroupConversationMessage, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        current_time = datetime.datetime.now()
        message = text_data_json["message"]
        room_name = text_data_json.get('room_name')
        sender = text_data_json.get('sender')
        await self.save_message(room_name, sender, message, current_time)
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "room_name":room_name,
                "sender":sender
            }
        )


    async def chat_message(self, event):
        message = event["message"]
        sender = event['sender']
        room_name = event['room_name']
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "room_name": room_name,
        }))

    @database_sync_to_async
    def save_message(self, room_name, sender, message, current_time):
        return GroupConversationMessage.objects.create(conversation_id=room_name, sender_id=sender, content=message, timestamp=current_time)


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        current_time = datetime.datetime.now()
        message = text_data_json["message"]
        room_name = text_data_json.get('room_name')
        sender = text_data_json.get('sender')
        image = text_data_json.get('image')
        print(image,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        await self.save_message(room_name, sender, message, current_time)
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "room_name":room_name,
                "sender":sender,
                "image":image,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event['sender']
        room_name = event['room_name']
        image = event['image']
        print(image, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "room_name": room_name,
            "image": image,
        }))

    @database_sync_to_async
    def save_message(self, room_name, sender, message, current_time):
        return GroupConversationMessage.objects.create(conversation_id=room_name, sender_id=sender, content=message, timestamp=current_time)
