from django.urls import path
from .views import TasksCommentListView, DeleteTaskCommentView, TasksCommentCreateView, TasksCommentUpdateView

app_name = 'task'
urlpatterns = [
    path('<int:pk>/comments', TasksCommentListView.as_view(), name='taskcomments'),
    path('comments/delete', DeleteTaskCommentView.as_view(), name='deletecomment'),
    path('<int:pk>/comments/create', TasksCommentCreateView.as_view(), name='createcomment'),
    path('<int:pk>/comments/update', TasksCommentUpdateView.as_view(), name='updatecomment'),
]
