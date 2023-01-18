import glob

import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import File
from project.models import Project
from task.models import Task
from user.models import *
from utils.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from guardian.core import ObjectPermissionChecker
from django.core.exceptions import PermissionDenied
import bugsnag


class DocumentProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        checker = ObjectPermissionChecker(request.user)
        project = get_object_or_404(Project, id=pk)
        files = File.objects.filter(project=project)
        tasks = Task.objects.filter(project=project)
        if checker.has_perm('olp_view_project', project):
            return render(request, 'projectdetails/files.html', {'project': project, 'files': files, 'tasks': tasks})
        else:
            raise PermissionDenied


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
        except Exception as e:
            bugsnag.notify(e)
            return HttpResponse('Bad Request', status=400)


class UploadFile(LoginRequiredMixin, View):
    def post(self, request):
        pass


class RenameFile(LoginRequiredMixin, View):
    def post(self, request):
        file_id = request.POST.get('file_id')
        new_name = request.POST.get('new_name')
        try:
            file = File.objects.get(id=file_id)
            list_path = file.file.url.split('/')[:-1][1:]
            path = os.path.join(*list_path)
            all_files = glob.glob(path + '/*')
            new_path = path + '/' + new_name
            if new_path in all_files:
                return HttpResponse('Bad request', status=400)
            else:
                os.rename('.' + file.file.url, './' + new_path)
                file.file.name = new_path.replace('media/', '')
                file.save()
                return HttpResponse('Successful', status=200)
        except File.DoesNotExist as e:
            bugsnag.notify(e)
            return HttpResponse('Not Found', status=404)
