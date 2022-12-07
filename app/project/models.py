from django.db import models
from user.models import User
from utils.models import ProgrammingLanguage, Currency
from ckeditor.fields import RichTextField


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name="project_collaborator")
    langcode_tags = models.ManyToManyField(ProgrammingLanguage, blank=True)
    cost = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    base = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Project'


def user_project_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/projects/project_{1}/{2}'.format(instance.project.created_by.id, instance.project.id, filename)


class File(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_project_directory_path, )
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
