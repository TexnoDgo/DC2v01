from django.utils.crypto import get_random_string

from .models import Order, Component, Position
from .component import check_component, create_component

from .handlers import qr_generator


# Создание позиции
def create_position(order_name, component_name, username, c_type, material_name, thickness, band_count, quantity,
                    mather_assembly, priority):
    try:
        code = get_random_string(length=13)
        print(code)
        qr_code = qr_generator(code)
        print("code done!")

        if check_component(component_name):
            order = Order.objects.get(title=order_name)
            component = Component.objects.get(title=component_name)
            position = Position(order=order, component=component, quantity=quantity, mather_assembly=mather_assembly,
                                priority=priority, code=code, qr_code=qr_code)
            position.save()
        else:
            order = Order.objects.get(title=order_name)
            component = create_component(component_name, username, c_type, material_name, thickness, band_count)
            position = Position(order=order, component=component, quantity=quantity, mather_assembly=mather_assembly,
                                priority=priority, code=code, qr_code=qr_code)
            position.save()
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
