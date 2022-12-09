from django.db import models

# Create your models here.

class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key = True)
    type = models.CharField(max_length = 50)
    vendor_name = models.CharField(max_length = 50)
    vendor_email = models.EmailField(max_length = 255)
    description = models.CharField(max_length = 500)
    location = models.CharField(max_length = 50)

class SensorReading(models.Model):
    id = models.AutoField(primary_key = True)
    sensor = models.ForeignKey(Sensor, on_delete = models.CASCADE)
    reading_type = models.CharField(max_length = 50)
    reading_value = models.CharField(max_length = 50)
    reading_date = models.DateField()
    description = models.CharField(max_length = 500)
    reading_time = models.CharField(max_length = 50)