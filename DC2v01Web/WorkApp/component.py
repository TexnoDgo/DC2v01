from .models import Order, Material, Component
from MainApp.models import Profile


# Проверка существования компонента
def check_component(component_name):
    try:
        component = Component.objects.get(title=component_name)
        return True
    except Exception:
        return False


# Создание компонента
def create_component(component_name, username, c_type, material_name, thickness, band_count):
    print(check_component(component_name))
    try:

        if check_component(component_name):
            return False
        else:
            profile = Profile.objects.get(user__username=username)
            material = Material.objects.get(title=material_name)
            component = Component(title=component_name, author=profile.user, c_type=c_type,
                                  material=material, thickness=thickness, band_count=band_count)
            component.save()
            return True
    except Exception:
        return False


# Редактирование компонента
def change_component(component_name, material, thickness, new_band):
    try:
        component = Component.objects.get(title=component_name)
        component.material = material
        component.thickness = thickness
        component.band_count = new_band
        component.save()

        return True
    except Exception:
        return False
