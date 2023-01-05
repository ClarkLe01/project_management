from django.urls import path
from .views import TasksCommentListView, DeleteTaskCommentView, TasksCommentCreateView, TasksCommentUpdateView, \
    UpdateTaskView, TaskApiView, DeleteTaskView

app_name = 'task'
urlpatterns = [
    path('<int:pk>/comments', TasksCommentListView.as_view(), name='taskcomments'),
    path('comments/delete', DeleteTaskCommentView.as_view(), name='deletecomment'),
    path('<int:pk>/comments/create', TasksCommentCreateView.as_view(), name='createcomment'),
    path('comments/<int:pk>/update', TasksCommentUpdateView.as_view(), name='updatecomment'),
    path('<int:pk>/update', UpdateTaskView.as_view(), name='updatetask'),
    path('delete', DeleteTaskView.as_view(), name='deletetask'),
    path('<int:pk>', TaskApiView.as_view(), name='retriveupdatedestroptask'),
]
