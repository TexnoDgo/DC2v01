from django.urls import path
from .views import MainAppClass

urlpatterns = [
    path('', MainAppClass.as_view()),

]
