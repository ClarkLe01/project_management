from django.db import models
from user.models import User
from utils.models import ProgrammingLanguage, Currency
from ckeditor.fields import RichTextField
from app.storage import OverwriteStorage
import os


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
        permissions = [
            ("olp_view_project", "OLP can view project"),
            ("olp_update_project", "OLP can update project"),
            ("olp_delete_project", "OLP can delete project"),
            ("olp_view_collaborator_project", "OLP can view project"),
            ("olp_add_collaborator_project", "OLP can add collaborator project"),
            ("olp_update_collaborator_project", "OLP can update collaborator project"),
            ("olp_delete_collaborator_project", "OLP can delete collaborator project"),
        ]
