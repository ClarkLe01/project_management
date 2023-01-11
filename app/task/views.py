from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from guardian.core import ObjectPermissionChecker
from guardian.mixins import LoginRequiredMixin
from rest_framework import generics
from .models import TaskComment, Task
from .serializers import TaskCommentSerializer, TaskKanbanSerializer
from project.models import Project
from user.models import User
from history.models import TaskHistory


# Create your views here.
class UpdateTaskView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        status = request.POST.get('task_status')
        task_title = request.POST.get('task_title')
        task_assign = request.POST.get('task_assign')
        due_date = request.POST.get('due_date')
        task_details = request.POST.get('task_details')
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
        TaskHistory.objects.create(task=task, user=request.user,
                                   action="updated", object="Task")
        return HttpResponse('Success', status=200)


class DeleteTaskView(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('task_id')
        if pk is not None and pk != '':
            task = get_object_or_404(Task, id=pk)
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


class TasksCommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        content = request.POST.get('comment')
        task = get_object_or_404(Task, id=pk)
        comment = TaskComment.objects.create(user=request.user, description=content, task=task)
        TaskHistory.objects.create(task=task, user=request.user,
                                   action="added", object="Comment",
                                   reference=comment.pk)
        return JsonResponse(TaskCommentSerializer(comment, many=False).data, status=201)


class TasksCommentUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        content = request.POST.get('comment')
        comment = get_object_or_404(TaskComment, id=pk)
        comment.description = content
        comment.save()
        return JsonResponse(TaskCommentSerializer(comment, many=False).data, status=200)


class DeleteTaskCommentView(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('comment_id')
        if pk is not None and pk != '':
            comment = get_object_or_404(TaskComment, id=pk)
            TaskHistory.objects.create(task=comment.task, user=request.user, action="deleted", object="Comment")
            comment.delete()
            return HttpResponse('Success', status=200)
        return HttpResponse('Bad Request', status=400)
