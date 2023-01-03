from rest_framework import serializers
from .models import User
from project.models import Project
from project.tasks.models import Task, TaskComment, TaskHistory
from user.serializers import AuthorSerializer


class TaskKanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'assignee', 'due_date', 'task_details']


class TaskCommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = TaskComment
        fields = '__all__'


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = '__all__'
