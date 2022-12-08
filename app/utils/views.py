from django.shortcuts import render  # noqa: 401
from django.conf import settings  # noqa: 401
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import ProgrammingLanguageSerializer, ProjectLangStatisticSerializer
from .models import ProgrammingLanguage
from django.db.models import Count, Q
from project.models import Project


class ProjectLangsView(viewsets.ViewSet, ListAPIView):
    serializer_class = ProgrammingLanguageSerializer
    queryset = ProgrammingLanguage.objects.all()


class ProjectLangsStatisticView(viewsets.ViewSet, ListAPIView):
    serializer_class = ProgrammingLanguageSerializer

    def get_queryset(self):
        return Project.objects.filter(Q(langcode_tags__isnull=False) & Q(created_by=self.request.user)).values(
            'langcode_tags__name').annotate(count=Count('*')).order_by('-count')
