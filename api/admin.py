from django.contrib import admin
from api import models

# Register your models here.
admin.site.register(models.UserInfo)
admin.site.register(models.UserToken)
admin.site.register(models.MachineRoom)
admin.site.register(models.PhysicalMachine)
admin.site.register(models.PhysicalDisk)
admin.site.register(models.VirtualMachine)
