# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datacenter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('active', models.BooleanField(default=0)),
                ('ip', models.IPAddressField(null=True, blank=True)),
                ('status', models.CharField(max_length=60, null=True, blank=True)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='task_history',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=100, null=True, blank=True)),
                ('image', models.CharField(max_length=100, null=True, blank=True)),
                ('instance_name', models.CharField(max_length=100, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('provider', models.CharField(max_length=200, null=True, blank=True)),
                ('telnet', models.BooleanField(default=0)),
                ('ssh', models.BooleanField(default=0)),
                ('netconf', models.BooleanField(default=0)),
                ('left_interface', models.CharField(max_length=200, null=True, blank=True)),
                ('right_interface', models.CharField(max_length=200, null=True, blank=True)),
                ('mng_interface', models.CharField(max_length=200, null=True, blank=True)),
                ('high_availability', models.CharField(max_length=100, null=True, blank=True)),
                ('auto_scaling', models.CharField(max_length=100, null=True, blank=True)),
                ('deep_analytics', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='vms',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('datacenter', models.ForeignKey(to='ngn_grid.Datacenter', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
