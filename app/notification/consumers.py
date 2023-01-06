import json

from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        user = self.scope["user"]
        if user.is_authenticated:
            self.groups.append("notifications-{}".format(user.pk))

    def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            self.groups.remove("notifications-{}".format(user.pk))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
