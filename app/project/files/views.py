import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import File
from project.models import Project
from project.tasks.models import Task
from user.models import *
from utils.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
import os


class DocumentProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        print(pk)
        project = get_object_or_404(Project, id=pk)
        files = File.objects.filter(project=project)
        tasks = Task.objects.filter(project=project)
        return render(request, 'projectdetails/files.html', {'project': project, 'files': files, 'tasks': tasks})


class DownloadFile(LoginRequiredMixin, View):
    def get(self, request, pk):
        file = File.objects.get(pk=pk)

        file_size_request = requests.get(request.scheme + '://' + request.META['HTTP_HOST'] + file.url(), stream=True)
        file_size = int(file_size_request.headers['Content-Length'])
        size = float(file_size / 1000000)
        size = round(size, 2)
        if size < 100:
            block_size = 1024
            filename = file.filename()
            with open(filename, 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    f.write(data)
                f.close()
            with open(filename, 'rb') as f:
                data = f.read()

            response = HttpResponse(data, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file.filename())
            return response
        return HttpResponse('Bad request', status=400)


class DeleteFile(LoginRequiredMixin, View):
    def post(self, request):
        try:
            delete_files = [int(x) for x in request.POST.get('delete_files').split(',')]
            files = File.objects.filter(id__in=delete_files)
            for file in files:
                print('.' + file.url())
                os.remove('.' + file.url())
                file.delete()
            return HttpResponse('Ok', status=200)
        except Exception:
            return HttpResponse('Bad Request', status=400)


class UploadFile(LoginRequiredMixin, View):
    def post(self, request):
        pass


class RenameFile(LoginRequiredMixin, View):
    def post(self, request):
        pass
