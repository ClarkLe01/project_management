from django.urls import path
from .views import ProjectLangsView, ProjectLangsStatisticView


app_name = 'utils'
urlpatterns = [
    path('projectlangs/', ProjectLangsView.as_view({'get': 'list'}), name='projectlangs'),
    path('projectlangstatistics/', ProjectLangsStatisticView.as_view({'get': 'list'}), name='projectlangstatistics'),
]
