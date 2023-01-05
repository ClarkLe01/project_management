from django.contrib import admin
from .models import TaskComment, Task
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(TaskComment, SimpleHistoryAdmin)
admin.site.register(Task, SimpleHistoryAdmin)
