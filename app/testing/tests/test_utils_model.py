from django.test import TestCase
from utils.models import Currency, ProgrammingLanguage


class CurrencyModelTests(TestCase):
    def setUp(self):
        self.code = 'USD'
        self.value = 1.0

    def test_create_currency(self):
        currency_instance = Currency.objects.create(code=self.code, value=self.value)
        self.assertEqual(currency_instance.code, self.code)
        self.assertEqual(currency_instance.value, self.value)
        self.assertEqual(str(currency_instance), self.code)


class ProgrammingLanguageModelTests(TestCase):
    def setUp(self):
        self.name = 'python'

    def test_create_currency(self):
        prolang_instance = ProgrammingLanguage.objects.create(name=self.name)
        self.assertEqual(prolang_instance.name, self.name)
        self.assertEqual(str(prolang_instance), self.name)
