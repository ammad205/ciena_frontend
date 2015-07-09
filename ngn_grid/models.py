__author__ = 'zaheerjan'

from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Datacenter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    active = models.BooleanField(default=0)
    ip = models.IPAddressField(null=True,blank=True)
    status = models.CharField(max_length=60,null=True,blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    description =  models.CharField(max_length=255, null=True, blank=True)


class vms(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    datacenter = models.ForeignKey(Datacenter ,null=True,blank=False)




class task_history(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)
    instance_name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    provider = models.CharField(max_length=200, null=True, blank=True)
    telnet = models.BooleanField( default=0)
    ssh = models.BooleanField(default=0)
    netconf = models.BooleanField(default=0)
    left_interface = models.CharField(max_length=200, null=True, blank=True)
    right_interface = models.CharField(max_length=200, null=True, blank=True)
    mng_interface = models.CharField(max_length=200, null=True, blank=True)
    high_availability = models.CharField(max_length=100, null=True, blank=True)
    auto_scaling = models.CharField(max_length=100, null=True, blank=True)
    deep_analytics = models.CharField(max_length=100, null=True, blank=True)


# test = Users(username = 'zaheer', email = 'zaheer@gmail.com', password = 'zaheer')
# print "!!!!!!!!!!!!!!!!!!", test.id , "!!!!!!!!!!!!!!!!!!!!!!!!!"
# test.save()
# print "!!!!!!!!!!!!!!!!!!", test.id , "!!!!!!!!!!!!!!!!!!!!!!!!!"

