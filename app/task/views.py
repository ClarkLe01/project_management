from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from guardian.mixins import LoginRequiredMixin
from rest_framework import generics

from .models import TaskComment
from project.tasks.models import Task

from .serializers import TaskCommentSerializer


# Create your views here.
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
        return JsonResponse(TaskCommentSerializer(comment, many=False).data, status=201)


class TasksCommentUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        content = request.POST.get('comment')
        comment = get_object_or_404(TaskComment, id=pk)
        comment.description = content
        comment.save()
        return HttpResponse('Success', status=200)


class DeleteTaskCommentView(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('comment_id')
        if pk is not None and pk != '':
            comment = get_object_or_404(TaskComment, id=pk)
            comment.delete()
            return HttpResponse('Success', status=200)
        return HttpResponse('Bad Request', status=400)
