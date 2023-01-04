from django.contrib import admin
from .models import TaskComment, TaskHistory
# Register your models here.
admin.site.register(TaskComment)
admin.site.register(TaskHistory)