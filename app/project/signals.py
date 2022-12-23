from .models import Project
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from utils.tasks import send_email


@receiver(post_save, sender=Project)
def notify_author(sender, instance, created, **kwargs):
    if created:
        mail_subject = 'Created New Project ID {0}'.format(instance.id)
        messages = "Project {0} created successful at {1}".format(instance.id, instance.created_date)
        send_email.delay(mail_subject, messages, recipients=[instance.created_by.email])
    else:
        mail_subject = 'Project ID {0} has a change'.format(instance.id)
        messages = "Project {0} updated at {1}".format(instance.id, instance.created_date)
        recipients = [recipient.email for recipient in instance.collaborators.all()]
        recipients.append(instance.created_by.email)
        send_email.delay(mail_subject, messages, recipients=recipients)


@receiver(m2m_changed, sender=Project.collaborators.through)
def add_collaborators(sender, instance, action, **kwargs):
    if action == 'post_add':
        # This will give you the users BEFORE any removals have happened
        recipients = [recipient.email for recipient in instance.collaborators.all()]
        print("Add collaborators to project", instance.collaborators.all())
        mail_subject = 'Invitation to join Project ID {0}'.format(instance.id)
        messages = "You are invited in Project {0} at {1}".format(instance.id, instance.created_date)
        send_email.delay(mail_subject, messages, recipients)
