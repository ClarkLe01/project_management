from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import TaskHistorySerializer
from .models import TaskHistory
from task.models import Task


# Create your views here.
class TasksHistoryListView(generics.ListAPIView):
    serializer_class = TaskHistorySerializer

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['pk'])
        return TaskHistory.objects.filter(task=task)
