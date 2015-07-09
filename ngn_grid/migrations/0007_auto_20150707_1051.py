# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngn_grid', '0006_auto_20150707_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vms',
            name='datacenter',
        ),
        migrations.DeleteModel(
            name='Datacenter',
        ),
        migrations.DeleteModel(
            name='vms',
        ),
    ]
