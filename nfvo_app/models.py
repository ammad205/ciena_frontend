__author__ = 'zaheerjanwar'

from django.db import models

class task_params(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    image = models.CharField(max_length=100)