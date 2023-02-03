import json
import random
from datetime import datetime, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import InvalidPage, EmptyPage, PageNotAnInteger
from django.urls import reverse
from project.models import Project
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..factories.project import ProjectFactory
from ..factories.user import UserFactory
from ..factories.utils import ProgrammingLanguageFactory, CurrencyFactory
from ..factories.file import FileFactory
from utils.tasks import updated_currency_exchange_rate


class CreateProjectViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory(password='testpassword')
        self.client = Client()
        self.url = reverse('project:projectdashboard')
        self.project = ProjectFactory(created_by=self.user)
        self.currency = CurrencyFactory()

    def test_create_project_successful(self):
        self.client.force_login(self.user)
        start = datetime.now()
        end = datetime.now() + timedelta(days=random.randint(1, 366))
        response = self.client.post(self.url, {
            'name': 'Test Project',
            'description': 'Test description',
            'start': start.strftime('%Y-%m-%d'),
            'end': end.strftime('%Y-%m-%d'),
            'collaborators': '[]',
            'langs': '[]',
            'cost': 4000,
            'base': 'USD',
        })
        self.assertEqual(response.status_code, 201)
        projects = Project.objects.filter(created_by=self.user)
        self.assertGreater(len(projects), 0)

    def test_create_project_successful_with_files(self):
        self.client.force_login(self.user)
        start = datetime.now()
        end = datetime.now() + timedelta(days=random.randint(1, 366))
        response = self.client.post(self.url, {
            'name': 'Test Project',
            'description': 'Test description',
            'start': start.strftime('%Y-%m-%d'),
            'end': end.strftime('%Y-%m-%d'),
            'collaborators': '[]',
            'langs': '[]',
            'cost': 4000,
            'base': 'USD',
            'files': SimpleUploadedFile('file_test.txt', b"file_content"),
        })
        self.assertEqual(response.status_code, 201)
        projects = Project.objects.filter(created_by=self.user)
        self.assertGreater(len(projects), 0)

    def test_create_project_failed(self):
        self.client.force_login(self.user)
        start = datetime.now()
        end = datetime.now() + timedelta(days=random.randint(1, 366))
        response = self.client.post(self.url, {
            'name': 'Test Project',
            'description': 'Test description',
            'start': start.strftime('%Y-%m-%d'),
            'end': end.strftime('%Y-%m-%d'),
            'collaborators': '[100, 200]',
            'langs': '[]',
            'cost': 4000,
            'base': 'USD',
        })
        self.assertEqual(response.status_code, 400)

    def test_get_view_with_no_query(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'projectmanagement/projectlist.html')
        self.assertEqual(response.status_code, 200)

    def test_get_view_with_query_name(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, {'name': self.project.name})
        self.assertEqual(response.status_code, 200)

        projects = Project.objects.filter(name=self.project.name)
        self.assertEqual(len(response.context['own_projects']), len(projects))

    def test_get_view_with_query_status(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, {'status': 0})
        self.assertEqual(response.status_code, 200)

        projects = Project.objects.filter(status=0)
        self.assertEqual(len(response.context['own_projects']), len(projects))

    def test_get_view_with_query_start(self):
        ProjectFactory(start_date=datetime.now(), created_by=self.user)
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, {'start': datetime.now().strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)

        projects = Project.objects.filter(start_date__gte=datetime.now())
        self.assertEqual(len(response.context['own_projects']), len(projects))

    def test_get_view_with_query_end(self):
        ProjectFactory(end_date=datetime.now(), created_by=self.user)
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, {'end': datetime.now().strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)

        projects = Project.objects.filter(end_date__lte=datetime.now())
        self.assertEqual(len(response.context['own_projects']), len(projects))

    def test_get_view_with_page_exception(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, {'page': 'a'})
        self.assertEqual(response.status_code, 200)


