from django.contrib import admin
from .models import *
from .forms import ProjectForm
from project.files.models import File
from guardian.admin import GuardedModelAdmin
from simple_history.admin import SimpleHistoryAdmin


class CollaboratorInline(admin.TabularInline):
    model = Project.collaborators.through


class LangCodeInline(admin.TabularInline):
    model = Project.langcode_tags.through


class ProjectsAdmin(GuardedModelAdmin):
    form = ProjectForm
    list_display = ['name', 'description', 'start_date', 'end_date', 'status', 'cost', 'base',
                    'created_by']
    list_filter = ['created_by__email', 'status', 'base']
    search_fields = ['name', 'created_by__email', ]
    inlines = [
        CollaboratorInline,
        LangCodeInline
    ]
    exclude = ('members', 'langcode_tags')


# Register your models here.
admin.site.register(Project, ProjectsAdmin)
admin.site.register(File)
