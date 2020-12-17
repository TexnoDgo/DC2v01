from django.urls import path
from .views import WorkAppClass

urlpatterns = [
    path('', WorkAppClass.as_view()),

]
