from MainApp.models import Profile
from .models import Project, Device


# Созданеи нового проекта для устройства
def create_project(device_name, project_name, username):
    try:
        device = Device.objects.get(title=device_name)
        profile = Profile.objects.get(user__username=username)
        project = Project(title=project_name, device=device, author=profile.user)
        project.save()
        return True
    except Exception:
        return False


# Выбор активного проекта для пользователя
def select_project(username, project_name):
    try:
        profile = Profile.objects.get(user__username=username)
        project = Project.objects.get(title=project_name)
        profile.active_project = project
        profile.save()
        return True
    except Exception:
        return False


# Изминение имени проекта
def change_project_name(project_name, project_name2):
    try:
        project = Project.objects.get(title=project_name)
        project.title = project_name2
        project.save()
        return True
    except Exception:
        return False


# Удаление проекта
def delete_project(project_name):
    try:
        project = Project.objects.get(title=project_name)
        project.delete()
        return True
    except Exception:
        return False


# Получение списка проектов и их устройств
def get_project_list_with_device():
    try:
        projects = Project.objects.all()
        return projects
    except Exception:
        return False


# Получение списка проектов для выбранного устройства
def get_project_list_for_device(device_name):
    try:
        print('Имя устройства: ' + device_name)
        '''devices = Device.objects.all()
        for device in devices:
            print(device)
            if device.title == device_name:
                print('True')'''
        device = Device.objects.get(title=device_name)
        print('Устройство в системе: ' + device.title)
        projects = Project.objects.filter(device=device)
        return projects
    except Exception:
        return False