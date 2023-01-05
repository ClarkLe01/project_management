from django.db.models.signals import pre_save
from django.dispatch import receiver
from simple_history.utils import update_change_reason
from .models import TaskComment


@receiver(pre_save, sender=TaskComment)
def log_change_task_comment(sender, instance, **kwargs):
    # Compare the current object with the old version
    old_object = sender.objects.get(pk=instance.pk)
    if instance.description != old_object.description:
        update_change_reason(instance, "Description changed")
