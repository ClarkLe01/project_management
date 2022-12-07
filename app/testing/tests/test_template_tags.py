from django.test import TestCase
from djangoProject1.templatetags.math_caculate import minus_int, add, convert_cost
from utils.models import Currency
from decimal import InvalidOperation, Decimal


class TemplateTagTests(TestCase):
    def test_minus_int(self):
        self.assertEqual(minus_int('1', 1), 0)
        self.assertEqual(minus_int('1', '2'), -1)

    def test_minus_int_with_exception(self):
        with self.assertRaises(ValueError, msg='Type Error of Number Input'):
            minus_int(1, 'a')

    def test_add_int(self):
        self.assertEqual(add('1', '2', '3'), 6)
        self.assertEqual(add(1, '2', '3'), 6)

    def test_add_int_with_exception(self):
        with self.assertRaises(ValueError, msg='Type Error of Number Input'):
            add(1, 2, '3', 'a')

    def test_convert_cost(self):
        Currency.objects.create(code='USD', value=1.0)
        Currency.objects.create(code='VND', value=24650.00)
        Currency.objects.create(code='EUR', value=0.97)

        self.assertEqual(convert_cost(60, 'EUR', 'VND'), str(round(float(60) * 24650.00 / 0.97, 2)) + ' ' + 'VND')
        self.assertEqual(convert_cost(60, 'EUR', 'USD'), str(round(float(60) * 1 / 0.97, 2)) + ' ' + 'USD')

    def test_convert_cost_with_exception(self):
        Currency.objects.create(code='USD', value=1.0)
        Currency.objects.create(code='VND', value=24650.00)
        Currency.objects.create(code='EUR', value=0.97)

        with self.assertRaises(InvalidOperation, msg='Type Error of Number Input'):
            convert_cost('asd', 'USD', 'VND')
