from django.urls import path, re_path
from .views import MainAppClass, project_page_view, orders_for_project_page_view, order_page_view

urlpatterns = [
    path('', MainAppClass.as_view()),
    path('project_page_view', project_page_view, name='project_page_view'),
    path(r'orders_for_project_view/<slug:pk>', orders_for_project_page_view, name='orders_for_project_view'),
    path(r'order_page_view/<slug:pk>', order_page_view, name='order_page_view'),

]
