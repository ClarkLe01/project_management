# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sessions.middleware import SessionMiddleware
# from django.core.signing import Signer
# from django.test import TestCase, RequestFactory, Client
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from user.login.views import LoginView
# from user.register.views import RegisterView
# from django.contrib.auth.models import AnonymousUser
# from rest_framework.test import APIClient
# from rest_framework import status
#
#
# class UserLoginViewTests(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.client = Client()
#         self.user = get_user_model().objects. \
#             create_user(email="test@example.com", password="test123",
#                         first_name="test", last_name="test")
#
#     def test_get_signin_view_as_anonymous_user(self):
#         response = self.client.get("/signin/")
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_signin_view_as_authenticated_user(self):
#         self.client.force_login(user=self.user)
#         response = self.client.get("/signin/")
#         self.assertRedirects(response, '/')
#
#     def test_successful_signin(self):
#         response = self.client.post("/signin/", {"email": "test@example.com", "password": "test123"})
#         self.assertEqual(response.status_code, 200)
#
#     def test_failed_signin(self):
#         response = self.client.post("/signin/", {"email": "testabc@example.com", "password": "test123"})
#         self.assertEqual(response.status_code, 401)
#
#
# class UserRegisterViewTests(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.client = Client()
#         self.user = get_user_model().objects. \
#             create_user(email="test@example.com", password="test123",
#                         first_name="test", last_name="test")
#
#     def test_get_signup_view_as_anonymous_user(self):
#         response = self.client.get("/signup/")
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_signup_view_as_authenticated_user(self):
#         self.client.force_login(user=self.user)
#         response = self.client.get("/signup/")
#         self.assertRedirects(response, '/')
#
#     def test_successful_signup(self):
#         response = self.client.post("/signup/", {
#             "email": "testabc@example.com",
#             "password": "test123",
#             'first_name': "test",
#             'last_name': "abc",
#         })
#         self.assertEqual(response.status_code, 200)
#
#     def test_failed_signup(self):
#         response = self.client.post("/signup/", {
#             "email": "test@example.com",
#             "password": "test123",
#             'first_name': "test",
#             'last_name': "test",
#         })
#         self.assertEqual(response.status_code, 409)
#
#
# class UserFogetPasswordViewTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = get_user_model().objects. \
#             create_user(email="test@example.com", password="test123",
#                         first_name="test", last_name="test")
#
#         self.signer = Signer(salt='extra')
#
#     def test_redirect_if_authenticated(self):
#         self.client.force_login(self.user)
#         response = self.client.get('/forgotPassword/')
#         self.assertRedirects(response, '/project/')
#
#     def test_get_view(self):
#         response = self.client.get('/forgotPassword/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_send_email_if_exists(self):
#         response = self.client.post('/forgotPassword/', {"email": "test@example.com"})
#         self.assertEqual(response.status_code, 200)
#
#     def test_send_email_if_not_exists(self):
#         response = self.client.post('/forgotPassword/', {"email": "testabasd@example.com"})
#         self.assertEqual(response.status_code, 400)
#
#     def test_get_resetpassword_view(self):
#         response = self.client.get('/resetPassword/')
#         self.assertEqual(response.status_code, 200)
#
#
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
