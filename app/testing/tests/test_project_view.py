from django.test import TestCase
from django.urls import reverse
from project.models import Project
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from datetime import datetime


class CreateProjectViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(first_name="Test", last_name="case",
                                                         email="test@example.com", password="test123")

    def test_create_project_list(self):
        self.client.force_login(self.user)
        response = self.client.post('/project/', {
            'name': 'Test Project',
            'description': 'Test description',
            'start': datetime.now().strftime('%Y-%m-%d'),
            'end': datetime.now().strftime('%Y-%m-%d'),
            'collaborators': '[]',
            'langs': '[]',
            'cost': 1.00,
            'base': 'USD',
        })
        self.assertEqual(response.status_code, 201)


class ProjectListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(first_name="Test", last_name="case",
                                                         email="test@example.com", password="test123")

    def test_get_list_project_view(self):
        self.client.force_login(self.user)
        response = self.client.get('/project/')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_get_list_project_view_with_params(self):
        self.client.force_login(self.user)
        response = self.client.get('/project/', {
            'name': 'A',
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/project/', {
            'status': 0,
        })
        self.assertEqual(response.status_code, 200)




class ProjectDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(first_name="Test", last_name="case",
                                                         email="test@example.com", password="test123")
        self.project = Project.objects.create(
            name="test_project",
            description="test description",
            start_date=datetime.now(),
            end_date=datetime.now(),
            created_by=self.user,
            cost=1.00,
            base='USD'
        )

    def test_get_project_by_id(self):
        self.client.force_login(self.user)
        url = reverse('project:detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_404_project_by_id(self):
        self.client.force_login(self.user)
        url = reverse('project:detail', args=[self.project.id + 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ProjectUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(first_name="Test", last_name="case",
                                                         email="test@example.com", password="test123")
        self.project = Project.objects.create(
            name="test_project",
            description="test description",
            start_date=datetime.now(),
            end_date=datetime.now(),
            created_by=self.user,
            cost=1.00,
            base='USD'
        )

    def test_update_get_project_by_id(self):
        self.client.force_login(self.user)
        url = reverse('project:update', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_get_404_project_by_id(self):
        self.client.force_login(self.user)
        url = reverse('project:update', args=[self.project.id + 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_post_project_by_id(self):
        self.client.force_login(self.user)
        url = reverse('project:update', args=[self.project.id])
        response = self.client.post(url, {
            'name': 'ok',
            'description': 'ok description',
            'start': datetime.now().strftime('%Y-%m-%d'),
            'end': datetime.now().strftime('%Y-%m-%d'),
            'cost': 5.00,
            'base': 'USD'
        })
        self.assertEqual(response.status_code, 200)


class DeleteProjectViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(first_name="Test", last_name="case",
                                                         email="test@example.com", password="test123")

    def test_delete_project_successful(self):
        project = Project.objects.create(
            name="test_project",
            description="test description",
            start_date=datetime.now(),
            end_date=datetime.now(),
            created_by=self.user,
            cost=1.00,
            base='USD'
        )
        self.client.force_login(self.user)
        url = reverse('project:delete', args=[project.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_project_failed(self):
        self.client.force_login(self.user)
        url = reverse('project:delete', args=[2])
        with self.assertRaises(Project.DoesNotExist, msg='Not exists project'):
            self.client.post(url)

    def test_delete_project_if_not_authenticated(self):
        url = reverse('project:delete', args=[2])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
