from rest_framework import serializers
from .models import TaskHistory
from user.serializers import AuthorSerializer
from task.serializers import TaskKanbanSerializer


class TaskHistorySerializer(serializers.ModelSerializer):
    user = AuthorSerializer()
    task = TaskKanbanSerializer()

    class Meta:
        model = TaskHistory
        fields = '__all__'
