from .models import Project
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from utils.tasks import send_email
from project.tasks.models import Task


@receiver(post_save, sender=Task)
def notify_author(sender, instance, created, **kwargs):
    pass


@receiver(pre_save, sender=Task)
def notify_author(sender, instance, created, **kwargs):
    pass
