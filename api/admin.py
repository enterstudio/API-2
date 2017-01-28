from django.contrib import admin
from api.models import Haus, Device, Sensor, UAC

admin.site.register(Haus)
admin.site.register(Device)
admin.site.register(Sensor)
admin.site.register(UAC)
# Register your models here.
