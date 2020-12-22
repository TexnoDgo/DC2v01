from django.urls import path, re_path
from .views import WorkAppClass, AddFileToComponent

urlpatterns = [
    path('', WorkAppClass.as_view()),
    re_path('addfile/(?P<filename>[^/]+)$', AddFileToComponent.as_view()),
]
