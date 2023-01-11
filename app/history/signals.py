import json
from asgiref.sync import async_to_sync
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import TaskHistory
from notification.models import Notification
import channels.layers


@receiver(post_save, sender=TaskHistory)
def notify_task_update(sender, instance, created, **kwargs):
    if instance.object == "Task":
        message = "{0} {1} {2} in Project {3}".format(instance.action, instance.object,
                                                      instance.task.id, instance.task.project.id)
    elif instance.object == "Comment":
        message = "{0} {1} in {2}".format(instance.action, instance.object, instance.task.title)
    else:
        message = "Something went wrong"

    participants = [user for user in instance.task.project.collaborators.all()]
    participants.append(instance.task.project.created_by)
    print(participants)
    print("Create notification")
    for user in participants:
        if user != instance.user:
            Notification.objects.create(message=message, user=user)

    # channel_layer = channels.layers.get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     f"user_{instance.project.created_by.pk}",
    #     {
    #         "type": "send_notification",
    #         "value": json.dumps(data)
    #     },
    # )
    # print(data)
