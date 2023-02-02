from django.shortcuts import render  # noqa: 401
from django.conf import settings  # noqa: 401
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from .serializers import ProgrammingLanguageSerializer
from .models import ProgrammingLanguage


class ProjectLangsView(viewsets.ViewSet, ListAPIView):
    serializer_class = ProgrammingLanguageSerializer
    queryset = ProgrammingLanguage.objects.all()
