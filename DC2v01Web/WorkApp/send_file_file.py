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
        print("Ошибка отправки PDF чертежа сомпонента")
        return False
