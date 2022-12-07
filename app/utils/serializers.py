from rest_framework import serializers
from .models import ProgrammingLanguage


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = ProgrammingLanguage
        fields = ['name']  # noqa: 501


class ProjectLangStatisticSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    count = serializers.IntegerField()

    class Meta:
        model = ProgrammingLanguage()
        fields = ['name', 'count']
