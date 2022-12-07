from .models import Project


def counter(request):
    project_count = 0
    if request.user.is_authenticated:
        projects = Project.objects.filter(created_by=request.user)
        project_count += len(projects)
    return dict(project_count=project_count)
