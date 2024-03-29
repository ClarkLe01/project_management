from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from rest_framework import generics
import bugsnag
from .models import Project
from project.files.models import File
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage, InvalidPage
from guardian.shortcuts import get_objects_for_user
from guardian.core import ObjectPermissionChecker
from django.core.exceptions import PermissionDenied
from task.serializers import TaskKanbanSerializer
from user.models import User
from utils.models import ProgrammingLanguage
from task.models import Task
from history.models import TaskHistory

PROJECT_PER_PAGE = 9


def get_project_object(idp, status=None):
    if status is None:
        return Project.objects.filter(created_by=idp)
    return Project.objects.filter(Q(created_by=idp) & Q(status=status))


class ProjectDashBoardView(LoginRequiredMixin, View):

    def get(self, request):
        projects = get_objects_for_user(request.user, 'project.olp_view_project', klass=Project)
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
        projects = projects.order_by("-updated_date")
        page = request.GET.get('page', 1)

        projects_paginator = Paginator(projects, PROJECT_PER_PAGE)
        try:
            projects = projects_paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            projects = projects_paginator.page(1)

        context = {
            'base': base,
            'query_string': query_string,
            'own_projects': projects,
            'completed_projects': get_project_object(idp=request.user.id, status=2),
            'pending_projects': get_project_object(idp=request.user.id, status=0),
            'inprogress_projects': get_project_object(idp=request.user.id, status=1)
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

        for _, file in dict(documents).items():
            File.objects.create(project=project, file=file[0])
        return HttpResponse('Created', status=201)


class ProjectViewDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        checker = ObjectPermissionChecker(request.user)
        project = get_object_or_404(Project, id=pk)
        tasks = Task.objects.filter(project=project)
        if checker.has_perm('olp_view_project', project):
            return render(request, 'projectdetails/overview.html', {'project': project, 'tasks': tasks})
        else:
            raise PermissionDenied


class UpdateProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        checker = ObjectPermissionChecker(request.user)
        project = get_object_or_404(Project, id=pk)
        tasks = Task.objects.filter(project=project)
        if checker.has_perm('olp_view_project', project):
            return render(request, 'projectdetails/settings.html', {'project': project, 'tasks': tasks})
        else:
            raise PermissionDenied

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
    checker = ObjectPermissionChecker(request.user)
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist as e:
        bugsnag.notify(e)
        e.skip_bugsnag = True
        raise e('Not exists project')

    if request.user.is_authenticated and checker.has_perm('olp_delete_project', project) and request.method == 'POST':
        project.delete()
        return redirect('/project')
    else:
        return HttpResponse('Bad request', status=404)


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
        TaskHistory.objects.create(task=task, user=request.user, action="added", object="Task")
        return HttpResponse('Created', status=201)


class TaskKanbanBoardApiView(generics.ListAPIView):
    serializer_class = TaskKanbanSerializer

    def get_queryset(self):
        return Task.objects.filter(project__id=self.kwargs['pk'])
