from rest_framework import serializers
from .models import User
from project.models import Project
from project.tasks.models import Task
from user.serializers import AuthorSerializer


class TaskKanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'assignee', 'due_date', 'task_details']
