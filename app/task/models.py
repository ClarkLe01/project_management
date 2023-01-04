from django.db import models
from user.models import User
from project.models import Project
from ckeditor.fields import RichTextField
from project.tasks.models import Task


# Create your models here.
class TaskComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    description = RichTextField()

    def __str__(self):
        return self.task.title


class TaskHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=255)
