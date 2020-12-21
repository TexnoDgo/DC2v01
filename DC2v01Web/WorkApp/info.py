from MainApp.models import Profile
from .models import Material, CuttingPlace, MachiningPlace, OtherPlace, Device


# Получение информации проекта, устиройства, заказа пользователя
def info(username):
    try:
        profile = Profile.objects.get(user__username=username)
        return profile
    except Exception:
        return False


# Получение списка материалов
def get_material_list():
    try:
        materials = Material.objects.all()
        return materials
    except Exception:
        return False


# Получение списка первичных операций
def first_operation_list():
    try:
        operations_list = []
        cutting_op_pl = CuttingPlace.objects.all()
        machining_op_pl = MachiningPlace.objects.all()
        other_op_pl = OtherPlace.objects.all()
        for cop in cutting_op_pl:
            operations_list.append(cop.title)
        for mop in machining_op_pl:
            operations_list.append(mop.title)
        for oop in other_op_pl:
            operations_list.append(oop.title)
        return operations_list
    except Exception:
        return False


# Получение списка устройств
def get_device_list():
    try:
        devices = Device.objects.all()
        return devices
    except Exception:
        return False
