from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import NotificationSerializer
from .models import Notification


# Create your views here.
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
