from django.db import models
from project.models import Project
from pyasn1.compat.octets import null
from task.models import Task, TaskComment
from user.models import User


# Create your models here.
class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    object = models.CharField(max_length=100)
    reference = models.IntegerField(default=-1)
    date = models.DateTimeField(auto_now_add=True)
