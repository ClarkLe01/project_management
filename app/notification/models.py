# myapp/models.py
from django.db import models
from user.models import User


class Notification(models.Model):
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user')
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='changed_by')

    def __str__(self):
        return self.user.email


class TestNotify(models.Model):
    user_sender = models.ForeignKey(User, null=True, blank=True, related_name='user_sender', on_delete=models.CASCADE)
    user_revoker = models.ForeignKey(User, null=True, blank=True, related_name='user_revoker', on_delete=models.CASCADE)
    status = models.CharField(max_length=264, null=True, blank=True, default="unread")
    type_of_notification = models.CharField(max_length=264, null=True, blank=True)
