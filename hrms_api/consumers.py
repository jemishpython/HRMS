# consumers.py
import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.db.models import Q

from hrms_api.models import GroupConversationMessage, PersonalConversationMessage, GroupMember, User, \
    PersonalConversation

Message_Type ={
    "MESSAGES": "MESSAGES",
    "ONLINE": "ONLINE",
    "OFFLINE": "OFFLINE",
    "IS_TYPING": "IS_TYPING",
    "NOT_TYPING": "NOT_TYPING",
}


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope['user']

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
        msg_type = text_data_json.get('msg_type')
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MESSAGE TYPE : ", msg_type)
        if msg_type == Message_Type['MESSAGES']:
            await self.save_message(room_name, sender, message, current_time)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": message,
                    "room_name":room_name,
                    "sender":sender
                }
            )
        elif msg_type == Message_Type['IS_TYPING']:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> IN TYPING")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_is_typing',
                    'sender': sender,
                }
            )
        elif msg_type == Message_Type["NOT_TYPING"]:
            await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                    'type': 'user_not_typing',
                    'sender' : sender,
                    }
                )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "msg_type":Message_Type['MESSAGES'],
            "message": event["message"],
            "sender": event['sender'],
            "room_name": event['room_name'],
        }))

    async def user_is_typing(self,event):
        await self.send(text_data=json.dumps({
            'msg_type': Message_Type['IS_TYPING'],
            'sender' : event['sender']
        }))

    async def user_not_typing(self,event):
        await self.send(text_data=json.dumps({
            'msg_type': Message_Type['NOT_TYPING'],
            'sender' : event['sender']
        }))

    @database_sync_to_async
    def save_message(self, room_name, sender, message, current_time):
        return PersonalConversationMessage.objects.create(conversation_id=room_name, sender_id=sender, content=message, timestamp=current_time)


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
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "room_name": room_name,
            "image": image,
        }))

    @database_sync_to_async
    def save_message(self, room_name, sender, message, current_time):
        room_name = GroupMember.objects.filter(group_id=room_name).first()
        return GroupConversationMessage.objects.create(conversation=room_name, sender_id=sender, content=message, timestamp=current_time)
