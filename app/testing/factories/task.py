from .user import UserFactory
from .project import ProjectFactory
from task.models import Task, TaskComment
import factory
from factory.fuzzy import FuzzyChoice
from faker import Faker

fake = Faker()


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    project = factory.SubFactory(ProjectFactory)
    title = factory.Faker('text')
    status = FuzzyChoice([Task.BACKLOG, Task.TODO, Task.WORKING, Task.DONE])
    due_date = factory.Faker('date_this_decade')
    task_details = factory.Faker('text')
    assignee = factory.SubFactory(UserFactory, is_active=True)


class TaskCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskComment

    user = factory.SubFactory(UserFactory)
    task = factory.SubFactory(TaskFactory)
    description = factory.Faker('text', max_nb_chars=255)
