from rest_framework import serializers
from .models import Notification
from user.serializers import AuthorSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()
    changed_by = AuthorSerializer()

    class Meta:
        model = Notification
        fields = '__all__'
