from django.urls import path
from .views import TasksHistoryListView

app_name = 'history'
urlpatterns = [
    path('task/<int:pk>', TasksHistoryListView.as_view(), name='taskhistory'),
]
