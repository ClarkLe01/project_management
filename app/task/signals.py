import json

from asgiref.sync import async_to_sync
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from simple_history.utils import update_change_reason
from .models import TaskComment, Task
from notification.consumers import NotificationConsumer
import channels.layers


@receiver(pre_save, sender=TaskComment)
def log_change_task_comment(sender, instance, **kwargs):
    # Compare the current object with the old version
    old_object = sender.objects.get(pk=instance.pk)
    if instance.description != old_object.description:
        update_change_reason(instance, "Description changed")


@receiver(pre_save, sender=Task)
def notify_update(sender, instance, **kwargs):
    data = 'Your Task has been updated!'
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "test_consumer_group",
        {
            "type": "send_notification",
            "value": json.dumps(data)
        },
    )
    print(data)
