from wsgiref.util import FileWrapper

from django.http import HttpResponse

from .models import Order, Project, Position, Component


# Функции отправки файла компонента
def send_comp_draw_pdf(component_name):
    try:
        component = Component.objects.get(title=component_name)
        draw = component.draw_pdf
        response = HttpResponse(FileWrapper(draw), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % '111.pdf'
        return response
    except Exception:
        print("Ошибка отправки PDF чертежа компонента")
        return False


def send_comp_draw_png(component_name):
    try:
        print("Начат процесс получение png чертежа компонента")
        component = Component.objects.get(title=component_name)
        draw = component.draw_pdf
        response = HttpResponse(FileWrapper(draw), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % '111.pdf'
        print("Процесс завершен!")
        return response
    except Exception:
        print("Ошибка отправки PNG чертежа компонента")
        return False