"""
Tests for user model.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..factories.user import UserFactory, SuperUserFactory


class UserModelTests(TestCase):
    """Test models."""

    def test_create_user(self):
        user = UserFactory(password='admin')
        self.assertIsInstance(user, get_user_model())
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.first_name)
        self.assertIsNotNone(user.last_name)
        self.assertTrue(user.check_password('admin'))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = UserFactory(email=email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', '1234')

    def test_create_superuser(self):
        """Test creating a superuser. """
        user = SuperUserFactory(email='admin@example.com')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, str(user))
