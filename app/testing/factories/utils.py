import random
from factory.fuzzy import FuzzyChoice
import factory
from utils.models import ProgrammingLanguage, Currency


class ProgrammingLanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgrammingLanguage

    name = FuzzyChoice(['Python', 'C/C++', 'ReactJs', 'Html', 'Golang'])


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency

    code = 'USD'
    value = 1
