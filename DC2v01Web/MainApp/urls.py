from django.urls import path, re_path
from .views import MainAppClass, project_page_view, orders_for_project_page_view, order_page_view,\
    check_operation_order, email

urlpatterns = [
    path('', MainAppClass.as_view()),
    path('project_page_view', project_page_view, name='project_page_view'),
    path(r'orders_for_project_view/<slug:pk>', orders_for_project_page_view, name='orders_for_project_view'),
    path(r'order_page_view/<slug:pk>', order_page_view, name='order_page_view'),
    path(r'check_operation_order/<slug:pk>/<slug:operation_pk>/<slug:operation_name>',
         check_operation_order, name='check_operation_order'),
    path(r'send_email/<slug:order>/<slug:operation>/<slug:identification>', email, name='send_email'),

]
