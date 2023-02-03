import factory
import random
from faker import Faker
from .project import ProjectFactory
from project.files.models import File

fake = Faker()


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = File

    project = factory.SubFactory(ProjectFactory)
    file = factory.django.FileField(filename=lambda _: fake.file_name(extension='pdf'))
    update_date = factory.Faker('date_time_this_decade')

    @factory.post_generation
    def file_extension(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            ext = extracted
        else:
            ext = random.choice(
                ['.jpg', '.png', '.jpeg', '.doc', '.docx', '.css', '.pdf', '.sql', '.xml', '.html', '.mp4', '.avi',
                 '.m4a', '.mp3'])
        self.file.name = fake.file_name(extension=ext.strip('.'))
