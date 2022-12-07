from .models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


_UNSAVED_FILEFIELD = 'unsaved_filefield'


@receiver(pre_save, sender=User)
def skip_saving_file(sender, instance=None, **kwargs):
    if not instance.id and not hasattr(instance, _UNSAVED_FILEFIELD):
        setattr(instance, _UNSAVED_FILEFIELD, instance.avatar)
        instance.avatar = None


@receiver(post_save, sender=User)
def save_file(sender, instance, created, **kwargs):
    if created and hasattr(instance, _UNSAVED_FILEFIELD):
        instance.avatar = getattr(instance, _UNSAVED_FILEFIELD)
        instance.save()
