from rest_framework import serializers
from .models import TaskComment, TaskHistory
from user.serializers import AuthorSerializer


class TaskCommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = TaskComment
        fields = '__all__'


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = '__all__'
