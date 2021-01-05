from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from WorkApp.models import Project, Order


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
def orders_for_project_view(request, pk):
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

# TODO: Добавить возможность объединять заказы для отправки
# TODO: Добавить генерацию таблиц заказов для аутсорсеров
# TODO: Добавить предпросмотра таблиц заказов для отправки и их редактирование
# TODO: Надеюсь все получится и все будет удобно!)
