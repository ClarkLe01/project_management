from copy import deepcopy

from user.models import User
import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda o: fake.email())
    username = deepcopy(email)
    first_name = factory.LazyAttribute(lambda o: fake.first_name())
    last_name = factory.LazyAttribute(lambda o: fake.last_name())
    password = factory.PostGenerationMethodCall('set_password', 'admin')
