from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from WorkApp.models import Project, Order, Position, OperationList, CuttingPlace, MachiningPlace, CoatingPlace,\
    OtherPlace


# TODO: Добавить функции
class MainAppClass(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            pass
            return Response(True)
        except Exception:
            return Response(False)


# TODO: Добавить страницу просмотра проектов
def project_page_view(request):
    try:
        projects = Project.objects.all()
    except Exception:
        projects = None

    context = {
        'projects': projects,
    }

    return render(request, 'MainApp/Project_Page_View.html', context)


# TODO: Добавить страницу просмотра заказов проектов
def orders_for_project_page_view(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        orders = Order.objects.filter(project=project)
    except Exception:
        pass

    context = {
        'project': project,
        'orders': orders,
    }

    return render(request, 'MainApp/Orders_For_Project_View.html', context)


# TODO: Добавить стриницу просмотра заказа общий, по операциям, по сборкам
def order_page_view(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        operations = OperationList.objects.filter(position__order=order)
        cutting_place = CuttingPlace.objects.all()
        machining_place = MachiningPlace.objects.all()
        coating_place = CoatingPlace.objects.all()
        other_place = OtherPlace.objects.all()
    except Exception:
        pass

    context = {
        'order': order,
        'operations': operations,
        'cutting_place': cutting_place,
        'machining_place': machining_place,
        'coating_place': coating_place,
        'other_place': other_place,
    }

    return render(request, 'MainApp/Order_Page_View.html', context)


# Странциа проверки операции заказа перед отправкой
def check_operation_order(request, pk, operation_name):
    try:
        order = Order.objects.get(pk=pk)
        positions = Position.objects.filter(order=order)

        if operation_name == 'НИИ Лазерная Резка' or operation_name == 'Сталь Плюс' or operation_name == 'Лазер ЛРМ'\
                or operation_name == 'Альянс Сталь':
            operation = CuttingPlace.objects.get(title=operation_name)
            operation_list = OperationList.objects.filter(cutting_place=operation)

        elif operation_name == 'CNC MetalWork' or operation_name == 'Опытынй завод':
            operation = MachiningPlace.objects.get(title=operation_name)
            operation_list = OperationList.objects.filter(machining_place=operation)

        elif operation_name == 'Другой':
            operation = OtherPlace.objects.get(title=operation_name)
            operation_list = OperationList.objects.filter(other_place=operation)

    except Exception:
        pass

    context = {
        'order': order,
        'operation': operation,
        'operation_list': operation_list,
    }

    return render(request, 'MainApp/Check_Operation_Order_Page_View.html', context)
# TODO: Добавить возможность объединять заказы для отправки
# TODO: Добавить генерацию таблиц заказов для аутсорсеров
# TODO: Добавить предпросмотра таблиц заказов для отправки и их редактирование
# TODO: Надеюсь все получится и все будет удобно!)
