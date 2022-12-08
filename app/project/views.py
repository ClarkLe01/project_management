from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Project
from user.models import *
from utils.models import *
from django.db.models import Q
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import ast

PROJECT_PER_PAGE = 2


def get_project_object(id, status=None):
    if status is None:
        return Project.objects.filter(created_by=id)
    return Project.objects.filter(Q(created_by=id) & Q(status=status))


class ProjectDashBoardView(LoginRequiredMixin, View):

    def get(self, request):
        projects = get_project_object(id=request.user.id)
        base = request.GET.get('base', 'USD')
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        name = request.GET.get('name', None)
        status = request.GET.get('status', None)
        query_string = ''
        if base:
            query_string += '&base={0}'.format(base)
        if name:
            query_string += '&name={0}'.format(name)
            projects = projects.filter(name__icontains=name)
        if start:
            query_string += '&start={0}'.format(start)
            projects = projects.filter(start_date__gte=start)
        if end:
            query_string += '&end={0}'.format(end)
            projects = projects.filter(end_date__lte=end)
        if status:
            query_string += '&status={0}'.format(status)
            projects = projects.filter(status=status)
        page = request.GET.get('page', 1)

        projects_paginator = Paginator(projects, PROJECT_PER_PAGE)
        try:
            projects = projects_paginator.page(page)
        except PageNotAnInteger:
            projects = projects_paginator.page(PROJECT_PER_PAGE)

        context = {
            'base': base,
            'query_string': query_string,
            'own_projects': projects,
            'completed_projects': get_project_object(id=request.user.id, status=2),
            'pending_projects': get_project_object(id=request.user.id, status=0),
            'inprogress_projects': get_project_object(id=request.user.id, status=1)
        }
        return render(request, 'projectmanagement/projectlist.html', context)

    def post(self, request):
        documents = request.FILES
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        langs = json.loads(request.POST.get('langs'))
        collaborators = json.loads(request.POST.get('collaborators'))
        cost = request.POST.get('cost')
        base = request.POST.get('base')
        user = User.objects.get(pk=request.user.id)
        try:
            collaborator_list = [User.objects.get(pk=int(user['value'])) for user in collaborators]
            lang_list = [ProgrammingLanguage.objects.get(name=lang['value']) for lang in langs]

        except TypeError:
            return HttpResponse('Bad Request', status=400)
        #
        # print(collaborator_list)
        project = Project.objects.create(name=name,
                                         description=description,
                                         start_date=start_date,
                                         end_date=end_date,
                                         created_by=user,
                                         cost=cost,
                                         base=base)
        project.collaborators.add(*collaborator_list)
        project.langcode_tags.add(*lang_list)
        project.save()
        for _, file in dict(documents).items():
            file_object = File.objects.create(project=project, file=file[0])
            print(file_object)
        return HttpResponse('Created', status=201)


class ProjectViewDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        return render(request, 'projectdetails/overview.html', {'project': project})


class UpdateProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        return render(request, 'projectdetails/settings.html', {'project': project})

    def post(self, request, pk):
        project = Project.objects.get(id=pk)
        project.name = request.POST.get('name')
        project.description = request.POST.get('description')
        project.start_date = request.POST.get('start')
        project.end_date = request.POST.get('end')
        project.cost = request.POST.get('cost')
        project.base = request.POST.get('base')
        project.save()
        return HttpResponse('Success', status=200)


def delete_project(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                Project.objects.get(id=pk).delete()
                return redirect('/project')
            except Project.DoesNotExist:
                raise Project.DoesNotExist('Not exists project')
    else:
        return HttpResponse('Bad request', status=404)
