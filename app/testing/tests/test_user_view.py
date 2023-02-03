from django.contrib.auth.tokens import default_token_generator
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.signing import Signer
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.login.views import LoginView
from user.register.views import RegisterView
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIClient
from rest_framework import status
from user.views import HomeView
from user.login.views import LoginView
from user.register.views import RegisterView
from ..factories.user import UserFactory
from django.core import mail


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_uses_correct_template(self):
        response = self.client.get('/')
        self.assertIs(response.resolver_match.func.view_class, HomeView)

    def test_home_view_contains_correct_context_data(self):
        response = self.client.get('/')
        # response = HomeView.as_view()(request)
        self.assertIs(response.resolver_match.func.view_class, HomeView)
        self.assertEqual(response.status_code, 200)


class UserLoginViewTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.user = UserFactory(email="test@example.com", password="test123")

    def test_get_signin_view_as_anonymous_user(self):
        response = self.client.get("/signin/")
        self.assertIs(response.resolver_match.func.view_class, LoginView)
        self.assertEqual(response.status_code, 200)

    def test_get_signin_view_as_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get("/signin/")
        self.assertRedirects(response, '/')

    def test_successful_signin(self):
        response = self.client.post("/signin/", {"email": "test@example.com", "password": "test123"})
        self.assertEqual(response.status_code, 200)

    def test_failed_signin(self):
        response = self.client.post("/signin/", {"email": "testabc@example.com", "password": "test123"})
        self.assertEqual(response.status_code, 401)


class UserRegisterViewTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.user = UserFactory(email="test@example.com", password="test123")

    def test_get_signup_view_as_anonymous_user(self):
        response = self.client.get("/signup/")
        self.assertIs(response.resolver_match.func.view_class, RegisterView)
        self.assertEqual(response.status_code, 200)

    def test_get_signup_view_as_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get("/signup/")
        self.assertRedirects(response, '/')

    def test_successful_signup(self):
        response = self.client.post("/signup/", {
            "email": "testabc@example.com",
            "password": "test123",
            'first_name': "test",
            'last_name': "abc",
        })
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(email='testabc@example.com')
        self.assertEqual(user.email, "testabc@example.com")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "abc")
        self.assertTrue(user.check_password('test123'))

    def test_failed_signup(self):
        response = self.client.post("/signup/", {
            "email": "test@example.com",
            "password": "test123",
            'first_name': "test",
            'last_name': "test",
        })
        self.assertEqual(response.status_code, 409)


class ForgotPasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.forgot_password_url = reverse('user:forgotPassword')
        self.user = UserFactory(email="test@example.com", password="test123")

    def test_forgot_password_view_with_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.forgot_password_url)
        self.assertRedirects(response, '/project/', status_code=302, target_status_code=200)

    def test_forgot_password_view_with_valid_email(self):
        response = self.client.post(self.forgot_password_url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password reset email has been sent to your email address.', response.content.decode())

    def test_forgot_password_view_with_invalid_email(self):
        response = self.client.post(self.forgot_password_url, {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn('Account does not exist!', response.content.decode())

    def test_forgot_password_view_with_get_request(self):
        response = self.client.get(self.forgot_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/reset_password/reset_password.html')
        self.assertIn('form', response.context)

# class UserUpdateViewTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = get_user_model().objects. \
#             create_user(email="test@example.com", password="test123",
#                         first_name="test", last_name="test")
#
#     def test_get_user_profile(self):
#         url = reverse('user:userprofile', kwargs={'pk': self.user.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_own_profile(self):
#         self.client.force_login(self.user)
#         response = self.client.get('/profile/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_updateprofile(self):
#         self.client.force_login(self.user)
#         response = self.client.get('/updateprofile/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_post_updateprofile(self):
#         self.client.force_login(self.user)
#         fname = 'change'
#         lname = 'change'
#         response = self.client.post('/updateprofile/', {
#             'fname': fname,
#             'lname': lname,
#         })
#         user = get_user_model().objects.get(id=self.user.id)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(user.first_name, fname)
#         self.assertEqual(user.last_name, lname)
#
#     def test_get_own_profile_if_not_authenticate(self):
#         response = self.client.get('/profile/')
#         self.assertEqual(response.status_code, 302)
#
#     def test_get_updateprofile_if_not_authenticate(self):
#         response = self.client.get('/updateprofile/')
#         self.assertEqual(response.status_code, 302)
#
#
# class UserLogoutViewTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = get_user_model().objects. \
#             create_user(email="test@example.com", password="test123",
#                         first_name="test", last_name="test")
#
#     def test_logout_user_view(self):
#         self.client.force_login(self.user)
#         response = self.client.get('/signout/')
#         self.assertEqual(response.status_code, 302)
#
#     def test_redirect_if_not_authenticated(self):
#         response = self.client.get('/signout/')
#         self.assertEqual(response.status_code, 302)
#
#
# class CollaboratorViewSetAPI(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects. \
#             create_user(email="test@example.com", password="test123",
#                         first_name="test", last_name="test")
#
#     def test_get_collaborator_api(self):
#         res = self.client.get(reverse('user:collaborator'))
#         self.assertEqual(res.status_code, 200)
#
#     def test_get_collaborator_api_if_authenticated(self):
#         self.client.force_authenticate(user=self.user)
#         res = self.client.get(reverse('user:collaborator'))
#         self.assertEqual(res.status_code, 200)
