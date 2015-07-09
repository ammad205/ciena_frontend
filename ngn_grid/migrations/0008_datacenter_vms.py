# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngn_grid', '0007_auto_20150707_1051'),
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
                ('state', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
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
