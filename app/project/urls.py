from django.urls import path, include
from user.login.views import LoginView
from user.register.views import RegisterView
from .views import (ProjectDashBoardView,
                    ProjectViewDetailView,
                    UpdateProjectView,
                    delete_project,
                    TasksProjectView,
                    TaskKanbanBoardApiView)
from project.files.views import DocumentProjectView, DownloadFile, DeleteFile

app_name = 'project'
urlpatterns = [
    path('', ProjectDashBoardView.as_view(), name='projectdashboard'),
    path('detail/<int:pk>', ProjectViewDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/update', UpdateProjectView.as_view(), name='update'),
    path('detail/<int:pk>/delete', delete_project, name='delete'),
    path('detail/<int:pk>/documents', DocumentProjectView.as_view(), name='documents'),
    path('downloadfile/<int:pk>', DownloadFile.as_view(), name='downloadfile'),
    path('deletefile/', DeleteFile.as_view(), name='deletefile'),
    path('detail/<int:pk>/tasks', TasksProjectView.as_view(), name='tasks'),
    path('detail/<int:pk>/tasklistapi', TaskKanbanBoardApiView.as_view(), name='tasklistapi'),
]
