from django.db import models
from user.models import User
from project.models import Project


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    BACKLOG = 'backlog'
    TODO = 'todo'
    WORKING = 'working'
    DONE = 'done'
    STATUS_CHOICES = [(BACKLOG, 'backlog'), (TODO, 'todo'), (WORKING, 'working'), (DONE, 'done')]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=BACKLOG)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField()
    task_details = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.project.name + ' - ' + self.title

