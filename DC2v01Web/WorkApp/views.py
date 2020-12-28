from random import random
from wsgiref.util import FileWrapper

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.http import HttpResponse

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from .info import info, get_material_list, first_operation_list, get_device_list
from .project import create_project, select_project, change_project_name, delete_project, get_project_list_with_device,\
    get_project_list_for_device, get_assembly_for_project
from .order import create_order, select_order, change_order_name, delete_order, get_order_list, order_assembly_list
from .component import create_component, change_component
from .position import create_position, real_position, change_position, delete_position, view_position,\
    change_operation_list, order_assembly_position_list, operation_list_for_position, check_position, \
    position_list_for_assembly
from .models import Component, OperationList
from .send_file_file import send_comp_draw_pdf, send_comp_draw_png


# TODO: Класс работы с запросами через JSON
class WorkAppClass(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            data = {}
            '''
            "request-type": "Вид запроса",
            "username": "Имя пользователя", 
            "component_name": "Имя компонента",
            "component_type": "Тип компонента",
            "assembly": "Имя материнской сборки",
            "material": "Имя материала детали",
            "thickness": "Толщина детали",
            "band": "Кол-во гибов",
            "quantity": "Кол-во деталей",
            "operation": "Операция",
            "project_name": "имя выделенного проекта",
            "project_name2": "новое имя проекта",
            "device_name": "имя устройства",
            "order_name": "имя выделенного заказа",
            "order_name2": "новое имя заказа"
            "priority": "приоритет изготовления позиции"
            '''
            request_type = request.data["request_type"]
            username = request.data["username"]
            component_name = request.data["component_name"]
            component_type = request.data["component_type"]
            assembly = request.data["assembly"]
            material = request.data["material"]
            thickness = request.data["thickness"]
            band = request.data["band"]
            quantity = request.data["quantity"]
            operation = request.data["operation"]
            project_name = request.data["project_name"]
            project_name2 = request.data["project_name2"]
            device_name = request.data["device_name"]
            order_name = request.data["order_name"]
            order_name2 = request.data["order_name2"]
            priority = request.data["priority"]

            # -----------------------Получение информации и списков (не редактируемых)------------------------
            if request_type == "info":
                try:
                    profile = info(username)
                    active_project = profile.active_project
                    project_device = active_project.device
                    active_order = profile.active_order
                    user = str(profile.user.username)
                    active_project = str(active_project)
                    project_device = str(project_device)
                    active_order = str(active_order)
                except Exception:
                    user = 'Пользователь не обраружен'
                    active_project = 'Активный проект'
                    project_device = 'Активное устройство'
                    active_order = 'Активный заказ'
                data = {
                    'user': user,
                    'active_project': active_project,
                    'project_device': project_device,
                    'active_order': active_order,
                }

            elif request_type == "material_list":
                material_list = get_material_list()
                i = 0
                for mat in material_list:
                    data[i] = mat.title
                    i += 1

            elif request_type == "operation_list":
                operations_place_list = first_operation_list()
                i = 0
                for operation in operations_place_list:
                    data[i] = operation
                    i += 1

            elif request_type == "device_list":
                devices = get_device_list()
                i = 0
                for dev in devices:
                    data[i] = dev.title
                    i += 1

            # --------------------------------------Действия с заказом----------------------------------------
            elif request_type == "order_list":
                orders = get_order_list(project_name)
                i = 0
                for order in orders:
                    data[i] = order.title
                    i += 1

            elif request_type == "create_order":
                data[0] = create_order(project_name, order_name, username)

            elif request_type == "active_order":
                data[0] = select_order(order_name, username)

            elif request_type == "change_order_name":
                data[0] = change_order_name(order_name, order_name2)

            elif request_type == "delete_order":
                data[0] = delete_order(order_name)

            elif request_type == "assembly_list_for_order":
                assembly = order_assembly_list(order_name)
                i = 0
                for asm in assembly:
                    data[i] = asm
                    i += 1

            # ----------------------------------- Действия с проектом -------------------------------------
            elif request_type == "select_active_project":
                data[0] = select_project(username, project_name)

            elif request_type == "create_project":
                data[0] = create_project(device_name, project_name, username)

            elif request_type == "project_list_with_device":
                projects = get_project_list_with_device()
                i = 0
                for project in projects:
                    mini_data = {"project": project.title, "device": project.device.title}
                    data[i] = mini_data
                    i += 1

            elif request_type == "change_project_name":
                data[0] = change_project_name(project_name, project_name2)

            elif request_type == "delete_project":
                data[0] = delete_project(project_name)

            elif request_type == "project_for_device":
                projects = get_project_list_for_device(device_name)
                i = 0
                for project in projects:
                    data[i] = project.title
                    i += 1

            elif request_type == "project_list":
                projects = get_project_list_with_device()
                i = 0
                for project in projects:
                    data[i] = project.title
                    i += 1

            elif request_type == "project_assembly":
                assembly = get_assembly_for_project(project_name)
                i = 0
                for asm in assembly:
                    data[i] = asm
                    i += 1

            # -----------------------------------Действия с компонентом-------------------------------
            elif request_type == "create_component":
                data[0] = create_component(component_name, username, component_type, material, thickness, band)

            elif request_type == "change_component":
                data[0] = change_component(component_name, material, thickness, band)

            # TODO: Добавить функцию получения информации о компоненте
            # TODO: Добавить функцию отдачи файлов компонента
            elif request_type == "component_info":
                component = Component.objects.get(title=component_name)
                print(component.author.username)
                print(component.create)
                print(component.c_type)
                print(component.material)
                print(component.thickness)
                print(component.band_count)
                data = {
                    "author": component.author.username,
                    "create": component.create,
                    "type": component.c_type,
                    "material": component.material,
                    "thickness": component.thickness,
                    "band_count": component.band_count
                }

            # ------------------------------------- Действия с позициями------------------------------
            elif request_type == "create_position":
                data[0] = create_position(order_name, component_name, username, component_type, material, thickness,
                                          band, quantity, assembly, priority, operation)

            elif request_type == "position_info":
                position = view_position(order_name, component_name, assembly)
                operation_data = operation_list_for_position(position)
                # TODO: Добавить полную информацию о позиции
                # TODO: Добавить функцию отдачи файлов позиции
                data = {
                    "quantity": position.quantity,
                    "operation": operation_data,
                    "priority": position.priority,
                    "code": position.code,
                }

            elif request_type == "change_position":
                data[0] = change_position(order_name, component_name, assembly, quantity, priority)

            elif request_type == "delete_position":
                data[0] = delete_position(order_name, component_name, assembly)

            elif request_type == "position_assembly_list_with_quantity":
                positions = real_position(order_name, component_name)
                i = 0
                for position in positions:
                    mini_data = {'mather_assembly': position.mather_assembly, 'quantity': position.quantity}
                    data[i] = mini_data
                    i += 1

            elif request_type == 'change_operation_list':
                data[0] = change_operation_list(order_name, component_name, assembly, operation)

            elif request_type == "position_list_for_assembly":
                positions = order_assembly_position_list(order_name, assembly)
                i = 0

                for position in positions:
                    mini_data = {position.component.title: position.quantity}
                    data[i] = mini_data
                    i += 1

            elif request_type == 'check_position':
                data[0] = check_position(order_name, component_name, assembly)

            elif request_type == "position_list_for_assembly2":
                data = position_list_for_assembly(project_name, assembly)

            '''
            else:
                pass'''
            return JsonResponse(data)
        except Exception:
            return Response(False)


# TODO: Класс добавления файлов
# TODO: Отработать все функции добавления файлов
class AddFileToComponent(APIView):
    parser_classes = [FileUploadParser, JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer]

    def put(self, request, filename, format=None):
        try:
            file_obj = request.data['file']
            print(filename)
            print(filename[-7:-1])
            # Если DXF-файл
            if filename[-4:-1] == 'DXF' or filename[-4:-1] == 'dxf':
                print('addDXF')
                component_name = filename[:-5]
                component = Component.objects.get(title=component_name)
                component.draw_pdf = file_obj
                component.save()

            # Если PDF-файл
            elif filename[-4:-1] == 'PDF' or filename[-4:-1] == 'pdf':
                print('addPDF')
                component_name = filename[:-5]
                component = Component.objects.get(title=component_name)
                a = random()
                b = a * 10000000000000
                c = str(b)[:13]
                file_obj.name = c + ".PDF"
                component.draw_pdf = file_obj
                component.save()

            # Если файл Детали или сборки
            elif filename[-7:-1] == 'SLDPRT' or filename[-7:-1] == 'sldprt' or filename[-7:-1] == 'SLDASM' \
                    or filename[-7:-1] == 'sldasm':
                print('addSLDPRT')
                component_name = filename[:-8]
                print(component_name)
                component = Component.objects.get(title=component_name)
                component.part_file = file_obj
                component.save()

            return Response(True)
        except Exception:
            return Response(False)


# TODO: Класс отпарвки файлов
class SendFile(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            '''
            request_type:
                component_draw_pdf
                component_draw_png
                component_dxf
                component_part
                
                order_table
                order_qr_code_list
                order_pdf_spec
                order_draw_archive
                order_dxf_archive
                order_part_archive
                
                project_pdf_spec
                
                position_qr_code            
                position_qr_code_prod            
                position_sticker            
                position_sticker_draw_pdf
            
            content_type:
                pdf - application/pdf
                dxf - image/vnd.dxf
                png - image/png
                sldprt - application/octet-stream
                sldasm - application/octet-stream
                xls - application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
                zip - application/zip
                
            '''
            request_type = request.data["request_type"]
            component_name = request.data["component_name"]
            c_type = request.data["component_type"]

            file = None

            # -----------------------------------------Действия с компонентом------------------------------------
            # Если запрос файла - PDF-чертеж компонента
            if request_type == "component_draw_pdf":
                pass

            # Если запрос файла - PNG-чертеж компонента
            elif request_type == "component_draw_png":
                file = send_comp_draw_png(component_name)

            # Если запрос файла - DXF-файл компонента
            elif request_type == "component_dxf":
                pass

            # Если запрос файла - PART-файл или ASM-файл компонента
            elif request_type == "component_part":
                if c_type == "PART":
                    pass
                else:
                    pass
            # -----------------------------------------Действия с компонентом------------------------------------

            # -------------------------------------------Действия с заказом--------------------------------------
            #  Если запрос файла - таблица заказ
            elif request_type == "order_table":
                pass

            #  Если запрос файла - список кодов заказ
            elif request_type == "order_qr_code_list":
                pass

            #  Если запрос файла - спецификация заказа
            elif request_type == "order_pdf_spec":
                pass

            #  Если запрос файла - архив чертежей заказ
            elif request_type == "order_draw_archive":
                pass

            #  Если запрос файла - архив dxf заказа
            elif request_type == "order_dxf_archive":
                pass

            #  Если запрос файла - архив моделей заказа
            elif request_type == "order_part_archive":
                pass
            # -------------------------------------------Действия с заказом--------------------------------------

            # -------------------------------------------Действия с проектом--------------------------------------
            #  Если запрос файла - PDF-спецификая проекта
            elif request_type == "order_part_archive":
                pass

            # -------------------------------------------Действия с проектом--------------------------------------

            # -------------------------------------------Действия с позицией--------------------------------------
            #  Если запрос файла - PNG QR-код позиции
            elif request_type == "position_qr_code":
                pass

            #  Если запрос файла - PNG производственный QR-код позиции
            elif request_type == "position_qr_code_prod":
                pass

            #  Если запрос файла - PNG стикер позиции
            elif request_type == "position_sticker":
                pass

            #  Если запрос файла - PDF-чертеж производственого чертежа
            elif request_type == "position_sticker_draw_pdf":
                pass
            # -------------------------------------------Действия с позицией--------------------------------------


            return file
            #return True
        except Exception:
            return Response(False)
