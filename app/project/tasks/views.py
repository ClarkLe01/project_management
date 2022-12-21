from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from project.models import Project
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from project.tasks.serializers import TaskKanbanSerializer
from project.tasks.models import Task, TaskComment
from django.http import HttpResponse
from user.models import User

class TasksProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        tasks = Task.objects.filter(project=project)
        return render(request, 'projectdetails/tasks.html', {'project': project, 'tasks': tasks})

    def post(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        task_title = request.POST.get("task_title")
        assignee = User.objects.get(id= request.POST.get("task_assign"))
        due_date = request.POST.get("due_date")
        task_details = request.POST.get("task_details")
        task = Task.objects.create(
            project = project,
            title = task_title,
            assignee = assignee,
            due_date = due_date,
            task_details = task_details
        )
        return HttpResponse('Created', status=201)


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


class TaskApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskKanbanSerializer
    queryset = Task.objects.all()


