from django.test import TestCase
import os
from django.conf import settings

from app.storage import OverwriteStorage


class OverwriteStorageTestCase(TestCase):

    def setUp(self):
        self.storage = OverwriteStorage()
        self.test_file = "test_file.txt"

    def test_get_available_name_overwrite(self):
        # Create a test file in the storage
        with open(os.path.join(settings.MEDIA_ROOT, self.test_file), "w") as f:
            f.write("test content")

        # Check that the file exists
        self.assertTrue(self.storage.exists(self.test_file))

        # Get the available name
        available_name = self.storage.get_available_name(self.test_file)

        # Check that the file with the same name has been overwritten
        self.assertFalse(self.storage.exists(self.test_file))

    def test_get_available_name_no_overwrite(self):
        # Check that the file does not exist
        self.assertFalse(self.storage.exists(self.test_file))

        # Get the available name
        available_name = self.storage.get_available_name(self.test_file)

        # Check that the available name is the same as the input name
        self.assertEqual(available_name, self.test_file)

    def tearDown(self):
        # Remove the test file
        if self.storage.exists(self.test_file):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.test_file))
