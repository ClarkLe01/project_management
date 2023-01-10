# myapp/models.py
from django.db import models
from user.models import User


class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class TestNotify(models.Model):
    user_sender = models.ForeignKey(User, null=True, blank=True, related_name='user_sender', on_delete=models.CASCADE)
    user_revoker = models.ForeignKey(User, null=True, blank=True, related_name='user_revoker', on_delete=models.CASCADE)
    status = models.CharField(max_length=264, null=True, blank=True, default="unread")
    type_of_notification = models.CharField(max_length=264, null=True, blank=True)
