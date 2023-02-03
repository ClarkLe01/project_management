from django.conf import settings
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.signing import Signer
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.views import HomeView, CollaboratorViewSetAPI, LogoutView
from user.login.views import LoginView
from user.register.views import RegisterView
from user.profile.views import UserProfile, UpdateOwnProfile, OwnProfile, UpdatePass
from user.serializers import UserSerializer
from ..factories.user import UserFactory
from ..factories.project import ProjectFactory
from django.core import mail
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.uploadedfile import SimpleUploadedFile


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


class ResetPasswordValidateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(email='test@example.com', password='password123')
        self.uidb64 = Signer(salt='extra').sign(self.user.id)
        self.token = default_token_generator.make_token(self.user)

    def test_reset_password_validate_with_valid_credentials(self):
        response = self.client.get(
            reverse('user:resetpassword_validate', kwargs={'uidb64': self.uidb64, 'token': self.token})
        )
        self.assertRedirects(response, '/resetPassword/', status_code=302, target_status_code=200)

    def test_reset_password_validate_with_invalid_credentials(self):
        response = self.client.get(
            reverse('user:resetpassword_validate', kwargs={'uidb64': self.uidb64, 'token': 'invalid_token'})
        )
        self.assertRedirects(response, '/signin/', status_code=302, target_status_code=200)

        uidb64 = Signer(salt='extra').sign(9999)
        response = self.client.get(
            reverse('user:resetpassword_validate', kwargs={'uidb64': uidb64, 'token': 'invalid_token'})
        )
        self.assertRedirects(response, '/signin/', status_code=302, target_status_code=200)


class ResetPasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(email='testuser', password='secret')
        self.uidb64 = Signer(salt='extra').sign(self.user.id)
        self.session = SessionStore()
        self.session['uidb64'] = self.uidb64
        self.session.save()

    def test_reset_password_success(self):
        self.client.cookies[settings.SESSION_COOKIE_NAME] = self.session.session_key
        response = self.client.post('/resetPassword/', {
            'password': 'newsecret',
            'confirm_password': 'newsecret'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Ok')

    def test_reset_password_fail(self):
        self.client.cookies[settings.SESSION_COOKIE_NAME] = self.session.session_key
        response = self.client.post('/resetPassword/', {
            'password': 'newsecret',
            'confirm_password': 'secret'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Bad request')

    def test_reset_password_get_request(self):
        response = self.client.get(reverse('user:resetPassword'))
        self.assertTemplateUsed(response, 'authentication/reset_password/new_password.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_get_with_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('user:resetPassword'))
        self.assertEqual(response.status_code, 200)


class CollaboratorViewSetAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = UserFactory(password='password123')
        self.user2 = UserFactory(password='password123')
        self.user2 = UserFactory(password='password123', is_active=False)

    def test_authenticated_user(self):
        request = self.factory.get(reverse('user:collaborator'))
        force_authenticate(request, user=self.user1)

        view = CollaboratorViewSetAPI.as_view()
        response = view(request)

        expected = get_user_model().objects.filter(Q(is_active=True) & ~Q(id=self.user1.id)).order_by('id')  # noqa: 501
        serializer = UserSerializer(expected, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_unauthenticated_user(self):
        request = self.factory.get(reverse('user:collaborator'))

        view = CollaboratorViewSetAPI.as_view()
        response = view(request)

        expected = get_user_model().objects.filter(Q(is_active=True))
        serializer = UserSerializer(expected, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(password='secret')

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user:signout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/signin')
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = UserFactory()
        self.client = Client()
        self.project = ProjectFactory(created_by=self.user)

    def test_view_uses_correct_template(self):
        # Log in the test user
        self.client.force_login(user=self.user)

        # Get the user profile view for the test user
        response = self.client.get(reverse('user:userprofile', kwargs={'pk': self.user.id}))

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'userprofile/overview.html')

    def test_view_returns_correct_user_and_projects(self):
        # Log in the test user
        self.client.force_login(user=self.user)

        # Get the user profile view for the test user
        response = self.client.get(reverse('user:userprofile', kwargs={'pk': self.user.id}))

        # Check that the correct user and projects were returned in the context
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(list(response.context['projects']), [self.project])

    def test_view_uses_correct_ownprofile_template(self):
        # Log in the test user
        self.client.force_login(user=self.user)

        # Get the user profile view for the test user
        response = self.client.get(reverse('user:profile'))

        # Check that the correct user and projects were returned in the context
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(list(response.context['projects']), [self.project])


class UpdateOwnProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.url = reverse('user:updateprofile')

    def test_get_updateprofile_view_as_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        self.assertIs(response.resolver_match.func.view_class, UpdateOwnProfile)
        self.assertTemplateUsed(response, 'userprofile/settings.html')
        self.assertEqual(response.status_code, 200)

    def test_update_own_profile_with_authenticated_user(self):
        # Login the user
        self.client.force_login(user=self.user)

        # Send a POST request to the UpdateOwnProfile view
        response = self.client.post(
            self.url,
            {
                'fname': 'Test',
                'lname': 'User',
                'files': SimpleUploadedFile("file.jpg", b"file_content"),
            },
        )

        # Check that the response has a status code of 200 OK
        self.assertEqual(response.status_code, 200)

        user = get_user_model().objects.get(email=self.user.email)

        # Check that the user's first name and last name were updated
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

        # Check that the user's avatar was updated
        self.assertEqual(user.avatar.read(), b"file_content")

    def test_update_own_profile_with_empty_first_name(self):
        # Login the user
        self.client.force_login(user=self.user)

        # Send a POST request to the UpdateOwnProfile view with an empty first name
        response = self.client.post(
            self.url,
            {
                'lname': 'User',
            },
        )

        # Check that the response has a status code of 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the user's first name was not updated
        user = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(user.first_name, self.user.first_name)

        # Check that the user's last name was updated
        self.assertEqual(user.last_name, 'User')

    def test_update_own_profile_with_empty_last_name(self):
        # Log in a user
        self.client.force_login(user=self.user)

        # Send a POST request to the update own profile view with empty last name
        response = self.client.post(
            self.url,
            {
                'fname': 'John',
            }
        )

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the user's first name has been updated
        user = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(user.first_name, 'John')

        # Assert that the user's last name is not empty
        self.assertNotEqual(user.last_name, '')


class UpdatePassTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(password='testpassword')
        self.client = Client()
        self.client.force_login(user=self.user)
        self.url = reverse('user:updatepass')

    def test_update_password_with_valid_current_password(self):
        response = self.client.post(self.url, {'current_password': 'testpassword', 'new_password': 'newpassword'})
        user = get_user_model().objects.get(email=self.user.email)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')
        self.assertTrue(user.check_password('newpassword'))

    def test_update_password_with_invalid_current_password(self):
        response = self.client.post(self.url, {'current_password': 'invalidpassword', 'new_password': 'newpassword'})
        self.assertEqual(response.status_code, 400)
