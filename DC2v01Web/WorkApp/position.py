from django.utils.crypto import get_random_string

from .models import Order, Component, Position, CuttingPlace, MachiningPlace, OtherPlace, OperationList
from .component import check_component, create_component

from .handlers import qr_generator, qr_generator_production, create_modify_draw


# Создание позиции
def create_position(order_name, component_name, username, c_type, material_name, thickness, band_count, quantity,
                    mather_assembly, priority, operation):
    try:
        c_p = check_position(order_name, component_name, mather_assembly)
        if c_p:
            return False
        else:
            order = Order.objects.get(title=order_name)
            code = get_random_string(length=13)
            qr_code = qr_generator(code)
            qr_gen_prod = qr_generator_production(code)

            if check_component(component_name):
                component = Component.objects.get(title=component_name)

            else:
                component = create_component(component_name, username, c_type, material_name, thickness, band_count)

            position = Position(order=order, component=component, quantity=quantity, mather_assembly=mather_assembly,
                                priority=priority, code=code, qr_code=qr_code, qr_code_production=qr_gen_prod)
            position.save()

            # Если применяется существующий компонент и у него есть чертеж, тогда
            if component.draw_pdf != "COMPONENT_DRAW_PDF/default.pdf":
                create_modify_draw(component, position, order)

            # Создание списка операций
            create_operation_list(operation, position)

        return True
    except Exception:
        return False


# Просмотр позиции
def view_position(order_name, component_name, assembly):
    try:
        order = Order.objects.get(title=order_name)
        component = Component.objects.get(title=component_name)
        position = Position.objects.get(order=order, component=component, mather_assembly=assembly)
        return position
    except Exception:
        return False


# Изминение позиции (Кол-во компонентов, приоритет)
def change_position(order_name, component_name, assembly, new_quantity, new_priority):
    try:
        order = Order.objects.get(title=order_name)
        component = Component.objects.get(title=component_name)
        position = Position.objects.get(order=order, component=component, mather_assembly=assembly)
        position.quantity = new_quantity
        position.priority = new_priority
        position.save()

        return True
    except Exception:
        return False


# Удаление позиции
def delete_position(order_name, component_name, assembly):
    try:
        order = Order.objects.get(title=order_name)
        component = Component.objects.get(title=component_name)
        position = Position.objects.get(order=order, component=component, mather_assembly=assembly)
        position.delete()

        return True
    except Exception:
        return False


# Проверка существующих позиций
def real_position(order_name, component_name):
    try:
        component = Component.objects.get(title=component_name)
        order = Order.objects.get(title=order_name)
        positions = Position.objects.filter(order=order, component=component)

        return positions
    except Exception:
        return False


# Проверка существующей позиции
def check_position(order_name, component_name, assembly):
    try:
        order = Order.objects.get(title=order_name)
        component = Component.objects.get(title=component_name)
        position = Position.objects.get(order=order, component=component, mather_assembly=assembly)
        return True
    except Exception:
        return False


# Создание списка операций
def create_operation_list(operation_list, position):
    try:
        # Создание OperationList
        print('Создание листа операций')
        cutting_place = CuttingPlace.objects.all()
        for place in cutting_place:
            if place.title == operation_list:
                operation = OperationList(position=position, cutting=True, cutting_place=place)
                operation.save()

        machining_place = MachiningPlace.objects.all()
        for place in machining_place:
            if place.title == operation_list:
                operation = OperationList(position=position, machining=True, machining_place=place)
                operation.save()

        other_place = OtherPlace.objects.all()
        for place in other_place:
            if place.title == operation_list:
                operation = OperationList(position=position, other=True, other_place=place)
                operation.save()

        print('Конец создания листа операций')
        return True
    except Exception:
        return False


# Изминение списка операций
def change_operation_list(order_name, component_name, assembly, operation):
    try:
        order = Order.objects.get(title=order_name)
        component = Component.objects.get(title=component_name)
        position = Position.objects.get(order=order, component=component, mather_assembly=assembly)
        operation_list = OperationList.objects.get(position=position)

        cutting_place = CuttingPlace.objects.all()
        for place in cutting_place:
            if place.title == operation:
                operation_list.cutting = True
                operation_list.cutting_place = place
                operation_list.save()

        machining_place = MachiningPlace.objects.all()
        for place in machining_place:
            if place.title == operation:
                operation_list.machining = True
                operation_list.machining_place = place
                operation_list.save()

        other_place = OtherPlace.objects.all()
        for place in other_place:
            if place.title == operation:
                operation_list.other = True
                operation_list.other_place = place
                operation_list.save()

        return True
    except Exception:
        return False


# Получение списка позиций для сборки
def order_assembly_position_list(order_name, assembly):
    try:
        order = Order.objects.get(title=order_name)
        positions = Position.objects.filter(order=order, mather_assembly=assembly)
        return positions
    except Exception:
        return False


# Получение списков операции по позиции
def operation_list_for_position(position):
    try:
        operation_list = OperationList.objects.get(position=position)
        operation_data = {}
        if operation_list.cutting:
            operation_data["cutting"] = operation_list.cutting_place.title
        if operation_list.machining:
            operation_data["machining"] = operation_list.machining_place.title
        if operation_list.coating:
            operation_data["coating"] = operation_list.coating_place.title
        if operation_list.other:
            operation_data["other"] = operation_list.other_place.title

        return operation_data
    except Exception:
        return False
