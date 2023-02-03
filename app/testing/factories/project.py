import random
from datetime import timedelta
import factory
from factory.fuzzy import FuzzyChoice
from project.models import Project
from .user import UserFactory
from .utils import ProgrammingLanguageFactory
from faker import Faker

fake = Faker()


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('name')
    description = factory.Faker('text')
    start_date = factory.Faker('date_this_decade')
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=random.randint(1, 366)))
    created_by = factory.SubFactory(UserFactory)
    collaborators = factory.SubFactory(UserFactory, blank=True, null=True)
    langcode_tags = factory.SubFactory(ProgrammingLanguageFactory, blank=True, null=True)
    status = FuzzyChoice([0, 1, 2])
    cost = factory.Faker('pydecimal', min_value=0, max_value=10000, right_digits=2)
    base = 'USD'

    @factory.post_generation
    def collaborators(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for collaborator in extracted:
                self.collaborators.add(collaborator)

    @factory.post_generation
    def langcode_tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for langcode in extracted:
                self.langcode_tags.add(langcode)
