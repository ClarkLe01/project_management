from django.urls import path
from .views import ProjectLangsView, ProjectLangsStatisticView


app_name = 'utils'
urlpatterns = [
    path('projectlangs/', ProjectLangsView.as_view({'get': 'list'}), name='projectlangs'),
]
