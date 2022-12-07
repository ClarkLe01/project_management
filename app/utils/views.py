from django.shortcuts import render  # noqa: 401
from django.conf import settings  # noqa: 401
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import ProgrammingLanguageSerializer, ProjectLangStatisticSerializer
from .models import ProgrammingLanguage
from django.db.models import Count
from project.models import Project


class ProjectLangsView(viewsets.ViewSet, ListAPIView):
    serializer_class = ProgrammingLanguageSerializer
    queryset = ProgrammingLanguage.objects.all()


class ProjectLangsStatisticView(viewsets.ViewSet, ListAPIView):
    serializer_class = ProgrammingLanguageSerializer
    queryset = Project.objects.exclude(langcode_tags=None).\
        values('langcode_tags').annotate(count=Count('*')).order_by('-count')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)