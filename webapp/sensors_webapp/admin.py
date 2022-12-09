from django.contrib import admin
from .models import Sensor, SensorReading
# Register your models here.

admin.site.register(Sensor)
admin.site.register(SensorReading)