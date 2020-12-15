from django.db import models

# Create your models here.


class GasDetails(models.Model):
    gasId = models.AutoField(primary_key=True)
    state = models.CharField(max_length=100)
    value = models.FloatField()
    gas = models.CharField(max_length=20)
    date = models.DateField()


class LiveDetails(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    gas = models.CharField(max_length=50)
    value = models.FloatField()
