from .user import UserFactory
from .project import ProjectFactory
from task.models import Task, TaskComment
import factory
from faker import Faker

fake = Faker()


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    project = factory.SubFactory(ProjectFactory)
    title = Faker('sentence')
    status = Task.BACKLOG
    due_date = Faker('date_this_decade')
    task_details = Faker('sentence')
    assignee = factory.SubFactory(UserFactory, is_active=True)
