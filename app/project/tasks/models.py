from django.db import models
from user.models import User
from project.models import Project


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    BACKLOG = 'backlog'
    INPROCESS = 'inprocess'
    WORKING = 'working'
    DONE = 'done'
    STATUS_CHOICES = [(BACKLOG,'backlog'), (INPROCESS,'inprocess'), (WORKING,'working'), (DONE,'done')]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=BACKLOG)
    assignee = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    target_details = models.CharField(max_length=255)

    def __str__(self):
        return self.project.name+' - '+self.title

class TaskComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.task.title