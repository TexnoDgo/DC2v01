from django.contrib import admin
from .models import Device, Project, Order, Component, Material, Color, Position, CuttingPlace, MachiningPlace,\
    CoatingPlace, OperationList, OtherPlace

admin.site.register(Device)
admin.site.register(Project)
admin.site.register(Order)
admin.site.register(Component)
admin.site.register(Material)
admin.site.register(Color)
admin.site.register(Position)
admin.site.register(CuttingPlace)
admin.site.register(MachiningPlace)
admin.site.register(CoatingPlace)
admin.site.register(OperationList)
admin.site.register(OtherPlace)
