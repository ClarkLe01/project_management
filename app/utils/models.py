from django.db import models


# Create your models here.

class Currency(models.Model):
    code = models.CharField(max_length=10, default='USD', unique=True)
    value = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


"""
from django.db.models import Count
statis = ProgrammingLanguage.objects.prefetch_related('project_set').all()
Project.objects.values('langcode_tags__name').annotate(count=Count('*')).order_by('-count')
Project.objects.exclude(langcode_tags=None).values('langcode_tags__name').annotate(count=Count('*')).order_by('-count')

"""