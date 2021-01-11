import os
from random import random
import zipfile
import io
from urllib.parse import unquote

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone


from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from WorkApp.models import Project, Order, Position, OperationList, CuttingPlace, MachiningPlace, CoatingPlace,\
    OtherPlace, Component

from .models import Profile

from .handlers import create_operation_table

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
def check_operation_order(request, pk, operation_pk, operation_name):
    try:
        order = Order.objects.get(pk=pk)
        positions = Position.objects.filter(order=order)

        if operation_name == 'cut':
            operation_name2 = CuttingPlace.objects.get(pk=operation_pk)
        elif operation_name == 'mach':
            operation_name2 = MachiningPlace.objects.get(pk=operation_pk)
        elif operation_name == 'oth':
            operation_name2 = OtherPlace.objects.get(pk=operation_pk)

        operation_name2 = str(operation_name2)

        operation = None
        operation_list = None

        if operation_name2 == 'НИИ Лазерная Резка' or operation_name2 == 'Сталь Плюс' or operation_name2 == 'Лазер ЛРМ'\
                or operation_name2 == 'Альянс Сталь':
            operation = CuttingPlace.objects.get(title=operation_name2)
            operation_list = OperationList.objects.filter(cutting_place=operation)

        elif operation_name2 == 'CNC MetalWork' or operation_name2 == 'Опытынй завод':
            operation = MachiningPlace.objects.get(title=operation_name2)
            operation_list = OperationList.objects.filter(machining_place=operation)

        elif operation_name2 == 'Другой':
            operation = OtherPlace.objects.get(title=operation_name2)
            operation_list = OperationList.objects.filter(other_place=operation)

    except Exception:
        pass

    context = {
        'order': order,
        'operation': operation,
        'operation_list': operation_list,
    }

    return render(request, 'MainApp/Check_Operation_Order_Page_View.html', context)


# Функция отправки сообщения для аутсорсеров
def email(request, order, operation, identification):
    send_order = Order.objects.get(pk=order)

    # --------------------------------------- Создание архива ---------------------------------------------
    try:
        a = random()
        b = a * 10000000000000
        c = str(b)[:13]

        zip_filename = "%s.zip" % c

        zip_path = os.path.join(BASE_DIR, 'media/temp/') + zip_filename
        zip_path = zip_path.replace('/', '\\')
        zf = zipfile.ZipFile(zip_path, "w")

        if identification == 'cut':
            operation_name = CuttingPlace.objects.get(pk=operation)
            operation_lists = OperationList.objects.filter(cutting_place=operation_name, position__order=send_order)
        elif identification == 'mach':
            operation_name = MachiningPlace.objects.get(pk=operation)
            operation_lists = OperationList.objects.filter(machining_place=operation_name, position__order=send_order)
        elif identification == 'oth':
            operation_name = OtherPlace.objects.get(pk=operation)
            operation_lists = OperationList.objects.filter(other_place=operation_name, position__order=send_order)

        table = create_operation_table(operation_lists, send_order)

        for one_operation in operation_lists:

            if str(one_operation.position.component.draw_pdf.url)[-11:-4] != 'default':
                draw_path = str(one_operation.position.component.draw_pdf.path).replace('/', '\\')
                draw_name = str(one_operation.position.component.draw_pdf).replace('/', '\\').\
                    replace('COMPONENT_DRAW_PDF', '')

                zf.write(draw_path, draw_name)

            elif str(one_operation.position.component.dxf_file.url)[-11:-4] != 'default':
                dxf_path = str(one_operation.position.component.dxf_file.path).replace('/', '\\')
                dxf_name = str(one_operation.position.component.dxf_file).replace('/', '\\').\
                    replace('COMPONENT_DXF_FILE', '')

                zf.write(dxf_path, dxf_name)

            elif str(one_operation.position.component.part_file.url)[-11:-4] != 'default':
                part_path = str(one_operation.position.component.part_file.path).replace('/', '\\')
                part_name = str(one_operation.position.component.part_file).replace('/', '\\').\
                    replace('COMPONENT_PART_FILE\\', '')

                zf.write(part_path, part_name)

        zf.close()

        # ----------------------------------- Подготовка информацяии для отправки письма ------------------------------
        try:
            user = send_order.author
            profile = Profile.objects.get(user=user)
            user_email = profile.new_email
            user_phone = profile.phone
            user_name = profile.profile_user_name
            user_last = profile.profile_user_last
        except Exception:
            print('Ошибка получения пользователя или профиля')

        # Тело отправеки сообщения
        subject = 'НИИ лазерных технологий'
        message = r' Добрый день, прошу выставить счет на изготовление следующих компонентов. <br>' \
                  ' Файлы для изготовления находятся внутри архива. <br>' \
                  ' Информация о деталях в прикрепленной таблице. <br>' \
                  ' ------------------------------------------------------------------------- <br>' \
                  ' C уважением, <br>' \
                  ' {0} {1} <br>' \
                  ' Контактная email: {2} <br>' \
                  ' Контактый моб.: {3}'.format(user_name, user_last, user_email, user_phone)
        email_from = settings.EMAIL_HOST_USER

        print('Адрес доставки: ' + operation_name.email)

        recipient_list = [operation_name.email, ]
        contact_email = "net@net.com"

        email = EmailMessage(subject, message, contact_email, recipient_list, headers={'Reply-To': contact_email})
        email.content_subtype = 'html'

        email.attach_file(zip_path)
        email.attach_file(table)

    except Exception:
        pass

    email.send()

    return redirect(request.META['HTTP_REFERER'])

# TODO: Добавить возможность объединять заказы для отправки
# TODO: Добавить генерацию таблиц заказов для аутсорсеров
# TODO: Добавить предпросмотра таблиц заказов для отправки и их редактирование
# TODO: Надеюсь все получится и все будет удобно!)

