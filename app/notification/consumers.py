import json
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser

from .models import TestNotify
from user.models import User


@database_sync_to_async
def create_notification(receiver, typeof="task_created", status="unread"):
    notification_to_create = TestNotify.objects.create(user_revoker=receiver, type_of_notification=typeof)
    print('I am here to help')
    return (notification_to_create.user_revoker.username, notification_to_create.type_of_notification)


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except:
        return AnonymousUser()


# class NotificationConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add(
#             f"notifications",
#             self.channel_name
#         )
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             f"notifications",
#             self.channel_name
#         )
#
#     async def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         await self.channel_layer.group_send(
#             "notifications", {"type": "chat_message", "message": message}
#         )
#
#     async def chat_message(self, event):
#         message = event["message"]
#         await self.accept()
#         await self.send(text_data=json.dumps({"message": message}))
#
#     async def websocket_connect(self, event):
#         print('connected', event)
#         print('Am i finallyy here')
#         print(self.scope['user'].id)
#         print(self.scope['user'])
#         await self.accept()
#         await self.send(json.dumps({
#             "type": "websocket.send",
#             "message": "hello world"
#         }), close=False)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        print(self.scope)
        await self.accept()
        await self.send(json.dumps({
            "type": "websocket.send",
            "text": "hello world"
        }))
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.send(json.dumps({
            "type": "websocket.send",
            "text": "room made"
        }))

    async def websocket_receive(self, event):
        print(event)
        data_to_get = json.loads(event['text'])
        user_to_get = await get_user(int(data_to_get))
        print(user_to_get)
        get_of = await create_notification(user_to_get)
        self.room_group_name = 'test_consumer_group'
        channel_layer = get_channel_layer()
        await (channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "send_notification",
                "value": json.dumps(get_of)
            }
        )
        print('receive', event)

    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def send_notification(self, event):
        await self.send(json.dumps({
            "type": "websocket.send",
            "data": event
        }))
        print('I am here')
        print(event)
