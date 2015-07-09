# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngn_grid', '0004_auto_20150707_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vms',
            name='datacenter',
            field=models.ForeignKey(to='ngn_grid.datacenter', null=True),
            preserve_default=True,
        ),
    ]
