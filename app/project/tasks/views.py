from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from project.models import Project
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from project.tasks.serializers import TaskKanbanSerializer
from project.tasks.models import Task, TaskComment
from django.http import HttpResponse


class TasksProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        tasks = Task.objects.filter(project=project)
        return render(request, 'projectdetails/tasks.html', {'project': project, 'tasks': tasks})


class TaskKanbanBoardApiView(generics.ListAPIView):
    serializer_class = TaskKanbanSerializer

    def get_queryset(self):
        return Task.objects.filter(project__id=self.kwargs['pk'])


class UpdateTaskView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        status = request.POST.get('task_status')
        if status:
            task.status = status
        task.save()
        return HttpResponse('Success', status=200)

