from decimal import Decimal, InvalidOperation
from django import template
from utils.models import Currency
import math
from datetime import datetime

register = template.Library()


@register.simple_tag
def minus_int(a, b):
    try:
        value1 = int(a)
        value2 = int(b)
    except ValueError:
        raise ValueError('Type Error of Number Input')
    return value1 - value2


@register.simple_tag
def add(*args):
    try:
        s = 0
        for i in args:
            s += int(i)

    except ValueError:
        raise ValueError('Type Error of Number Input')
    return s


@register.simple_tag
def convert_cost(cost, base, target_code):
    try:
        ratio = Currency.objects.get(code=target_code).value / Currency.objects.get(code=base).value
        return str(round(Decimal(cost) * ratio, 2)) + ' ' + target_code
    except InvalidOperation:
        raise InvalidOperation('Type Error of Number Input')

