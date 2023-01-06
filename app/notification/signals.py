# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Notification
#
#
# @receiver(post_save, sender=MyModel)
# def send_notification(sender, instance, **kwargs):
#     # send a notification to the specific user
#     Notification.objects.create(
#         title="Object changed",
#         message=f"The object {instance.id} has been changed",
#         user=instance.user,
#     )


# @receiver(post_save, sender=Notification)
# def notify(sender, instance, created, **kwargs):
#     if created:
#         instance.group("notifications-{}".format(instance.recipient.pk)).send({
#             "text": instance.message
#         })
