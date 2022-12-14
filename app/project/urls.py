from django.urls import path, include
from user.login.views import LoginView
from user.register.views import RegisterView
from .views import *


app_name = 'project'
urlpatterns = [
    path('', ProjectDashBoardView.as_view(), name='projectdashboard'),
    path('detail/<int:pk>', ProjectViewDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/update', UpdateProjectView.as_view(), name='update'),
    path('detail/<int:pk>/delete', delete_project, name='delete'),
    path('documents/<int:pk>', DocumentProjectView.as_view(), name='documents'),
    path('downloadfile/<int:pk>', DownloadFile.as_view(), name='downloadfile'),
    path('deletefile/<int:pk>', DeleteFile.as_view(), name='deletefile')
]
