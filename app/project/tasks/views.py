from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from project.models import Project, File
from django.shortcuts import render, get_object_or_404


class TasksProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        return render(request, 'projectdetails/tasks.html', {'project': project})