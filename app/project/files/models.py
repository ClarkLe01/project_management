from django.db import models
from user.models import User
from project.models import Project
from app.storage import OverwriteStorage
import os


def user_project_directory_path(instance, filename):
    # files will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/projects/project_{1}/{2}'.format(instance.project.created_by.id, instance.project.id, filename)


class File(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(max_length=500, upload_to=user_project_directory_path, storage=OverwriteStorage())
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name)
    def url(self):
        return self.file.url
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    def size(self):
        x = self.file.size
        y = 512000
        if x < y:
            value = round(x / 1000, 2)
            ext = ' kb'
        elif x < y * 1000:
            value = round(x / 1000000, 2)
            ext = ' Mb'
        else:
            value = round(x / 1000000000, 2)
            ext = ' Gb'
        return str(value) + ext

    def icon_svg(self):
        def read_file(path):
            with open(path, 'r') as file:
                data = file.read().rstrip()
            return data

        def get_url_svg_icon(extension):
            ext_dict = {
                '.jpg': 'image.svg',
                '.png': 'image.svg',
                '.jpeg': 'image.svg',
                '.doc': 'doc.svg',
                '.docx': 'doc.svg',
                '.css': 'css.svg',
                '.pdf': 'pdf.svg',
                '.sql': 'sql.svg',
                '.xml': 'xml.svg',
                '.html': 'html.svg',
                '.mp4': 'video-file.svg',
                '.avi': 'video-file.svg',
                '.m4a': 'video-file.svg',
                '.mp3': 'video-file.svg',
            }
            if extension in ext_dict.keys():
                return './static/assets/media/svg/files/'+ext_dict[extension]
            return './static/assets/media/svg/files/undefined-file.svg'
        return read_file(get_url_svg_icon(self.extension()))
