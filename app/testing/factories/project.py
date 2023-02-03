from datetime import timedelta
import factory
from project.models import Project
from .user import UserFactory
from faker import Faker

fake = Faker()


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('name')
    description = factory.Faker('text')
    start_date = factory.Faker('date_this_decade')
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=365))
    created_by = factory.SubFactory(UserFactory)
    cost = factory.Faker('pydecimal', min_value=0, max_value=10000, right_digits=2)
