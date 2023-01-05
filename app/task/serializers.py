from rest_framework import serializers
from .models import Task, TaskComment
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
