from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Device(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(default=timezone.now)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    pdf_specification = models.FileField(upload_to='PROJECT_PDF_SPECIFICATION', default=None)

    def __str__(self):
        return self.title


class Order(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    readiness = models.DateField(null=True)
    table = models.FileField(upload_to="ORDERS_TABLE", default=None)
    qr_code_list = models.FileField(upload_to='ORDERS_QR_CODE_LIST', default=None)
    pdf_specification = models.FileField(upload_to='ORDER_PDF_SPECIFICATION', default=None)
    draw_archive = models.FileField(upload_to='ORDERS_DRAW_ARCHIVE', default=None)
    dxf_archive = models.FileField(upload_to='ORDERS_DXF_ARCHIVE', default=None)
    part_archive = models.FileField(upload_to='ORDERS_PART_ARCHIVE', default=None)

    def __str__(self):
        return self.title


# Таблица компонентов
class Component(models.Model):
    COMPONENT_TYPE = (
        ('PART', 'PART'),
        ('ASSEMBLY', 'ASSEMBLY')
    )
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(default=timezone.now)
    c_type = models.CharField(max_length=20, choices=COMPONENT_TYPE, default='PART')
    material = models.CharField(max_length=150, default='default')
    thickness = models.CharField(max_length=10, default='0')
    band_count = models.CharField(max_length=10, default='0')
    draw_pdf = models.FileField(upload_to='COMPONENT_DRAW_PDF', default='COMPONENT_DRAW_PDF/default.pdf', null=True)
    draw_png = models.FileField(upload_to='COMPONENT_DRAW_PNG', default='COMPONENT_DRAW_PNG/default.png', null=True)
    dxf_file = models.FileField(upload_to='COMPONENT_DXF_FILE', default='COMPONENT_DXF_FILE/default.png', null=True)
    part_file = models.FileField(upload_to='COMPONENT_PART_FILE', default='COMPONENT_PART_FILE/default.png', null=True)

    def __str__(self):
        return self.title


# Таблица материалов
class Material(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


# Таблица цветов
class Color(models.Model):
    title = models.CharField(max_length=100)
    hex_color = models.CharField(max_length=10)
    r_color = models.IntegerField()
    g_color = models.IntegerField()
    b_color = models.IntegerField()

    def __str__(self):
        return self.title


# Таблица позиций
class Position(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField()
    code = models.CharField(max_length=13)
    qr_code = models.FileField(upload_to='POSITION_QR_CODE', default=None)
    qr_code_production = models.FileField(upload_to='POSITION_QR_CODE_PRODUCTION', default=None)
    sticker = models.FileField(upload_to='POSITION_STICKER', default=None)
    sticker_draw_pdf = models.FileField(upload_to='POSITION_DRAW_PDF', default=None)
    mather_assembly = models.CharField(max_length=255, default='default')
    priority = models.IntegerField(default=0)
    storage = models.CharField(max_length=10, default="0", null=True)

    def __str__(self):
        return self.order.title + " - " + self.component.title


class CuttingPlace(models.Model):
    title = models.CharField(max_length=250)
    email = models.EmailField()
    identification = models.CharField(max_length=50, default='cut')

    def __str__(self):
        return self.title


class MachiningPlace(models.Model):
    title = models.CharField(max_length=250)
    email = models.EmailField()
    identification = models.CharField(max_length=50, default='mach')

    def __str__(self):
        return self.title


class CoatingPlace(models.Model):
    title = models.CharField(max_length=250)
    email = models.EmailField()
    identification = models.CharField(max_length=50, default='coa')

    def __str__(self):
        return self.title


class OtherPlace(models.Model):
    title = models.CharField(max_length=250)
    email = models.EmailField()
    identification = models.CharField(max_length=50, default='oth')

    def __str__(self):
        return self.title


class OperationList(models.Model):
    STATUS_TYPE = (
        ('NONE', 'NONE'),
        ('CREATE', 'CREATE'),
        ('WORK', 'WORK'),
        ('DONE', 'DONE'),
    )
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    cutting = models.BooleanField(default=False)
    cutting_place = models.ForeignKey(CuttingPlace, on_delete=models.CASCADE, null=True)
    cutting_status = models.CharField(max_length=20, choices=STATUS_TYPE, default='NONE')

    machining = models.BooleanField(default=False)
    machining_place = models.ForeignKey(MachiningPlace, on_delete=models.CASCADE, null=True)
    machining_status = models.CharField(max_length=20, choices=STATUS_TYPE, default='NONE')

    coating = models.BooleanField(default=False)
    coating_place = models.ForeignKey(CoatingPlace, on_delete=models.CASCADE, null=True)
    coating_status = models.CharField(max_length=20, choices=STATUS_TYPE, default='NONE')

    other = models.BooleanField(default=False)
    other_place = models.ForeignKey(OtherPlace, on_delete=models.CASCADE, null=True)
    other_status = models.CharField(max_length=20, choices=STATUS_TYPE, default='NONE')

    general_status = models.CharField(max_length=20, choices=STATUS_TYPE, default='CREATE')

    notes = models.CharField(max_length=255, default='None')

    def __str__(self):
        return self.position.component.title + "-operation"
