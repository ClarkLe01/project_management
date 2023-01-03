from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from project.models import Project
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from project.tasks.serializers import TaskKanbanSerializer, TaskCommentSerializer, TaskHistorySerializer
from project.tasks.models import Task, TaskComment, TaskHistory
from django.http import HttpResponse
from rest_framework.views import APIView
from user.models import User
from guardian.core import ObjectPermissionChecker
from django.core.exceptions import PermissionDenied


class TasksProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        checker = ObjectPermissionChecker(request.user)
        project = get_object_or_404(Project, id=pk)
        tasks = Task.objects.filter(project=project)
        if checker.has_perm('olp_view_project', project):
            return render(request, 'projectdetails/tasks.html', {'project': project, 'tasks': tasks})
        else:
            raise PermissionDenied

    def post(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        task_title = request.POST.get("task_title")
        assignee = User.objects.get(id=request.POST.get("task_assign"))
        due_date = request.POST.get("due_date")
        task_details = request.POST.get("task_details")
        task = Task.objects.create(
            project=project,
            title=task_title,
            assignee=assignee,
            due_date=due_date,
            task_details=task_details
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
        task_title = request.POST.get('task_title')
        task_assign = request.POST.get('task_assign')
        due_date = request.POST.get('due_date')
        task_details = request.POST.get('task_details')
        print(status, task_title, task_assign, task_details)
        if status is not None and status != '':
            task.status = status
        if task_title is not None and task_title != '':
            task.title = task_title
        if due_date is not None and due_date != '':
            task.due_date = due_date
        if task_assign is not None and task_assign != '':
            task.assignee = User.objects.get(id=task_assign)
        if task_details is not None and task_details != '':
            task.task_details = task_details
        task.save()
        return HttpResponse('Success', status=200)


class DeleteTaskView(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('task_id')
        if pk is not None and pk != '':
            task = get_object_or_404(Task, id=pk)
            print(task)
            task.delete()
            return HttpResponse('Success', status=200)
        return HttpResponse('Bad Request', status=400)


class TaskApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskKanbanSerializer
    queryset = Task.objects.all()


class TasksCommentListView(generics.ListAPIView):
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['pk'])
        return TaskComment.objects.filter(task=task)


class DeleteTaskCommentView(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('comment_id')
        if pk is not None and pk != '':
            comment = get_object_or_404(TaskComment, id=pk)
            comment.delete()
            return HttpResponse('Success', status=200)
        return HttpResponse('Bad Request', status=400)
