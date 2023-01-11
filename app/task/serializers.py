from rest_framework import serializers
from .models import Task, TaskComment
from user.serializers import AuthorSerializer
from project.serializers import ProjectSerializer


class TaskKanbanSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class TaskCommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = TaskComment
        fields = '__all__'
