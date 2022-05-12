from django.db import models
from datetime import date

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)

class Sensor(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=255, null=True)

class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    temp = models.FloatField()
    temp_date = models.DateField(auto_now=True)