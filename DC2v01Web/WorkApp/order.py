from MainApp.models import Profile
from .models import Order, Project


# Создание заказ
def create_order(project_name, order_name, username):
    try:
        project = Project.objects.get(title=project_name)
        profile = Profile.objects.get(user__username=username)
        order = Order(title=order_name, project=project, author=profile.user)
        order.save()
        return True
    except Exception:
        return False


# Выбор активного заказа для пользователя
def select_order(order_name, username):
    try:
        profile = Profile.objects.get(user__username=username)
        order = Order.obejects.get(title=order_name)
        profile.active_order = order
        profile.save()
        return True
    except Exception:
        return False


# Изминение имени заказа пользователем
def change_order_name(order_name, order_name2):
    try:
        return True
    except Exception:
        return False


# Удаление заказа
def delete_order(order_name):
    try:
        order = Order.objects.get(title=order_name)
        order.delete()
        return True
    except Exception:
        return False


# Получение списка заказов
def get_order_list(project_name):
    try:
        project = Project.objects.get(title=project_name)
        orders = Order.objects.filter(project=project)
        return orders
    except Exception:
        return False
