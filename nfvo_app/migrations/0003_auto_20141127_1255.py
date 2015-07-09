# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfvo_app', '0002_auto_20141127_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users_tasks',
            name='username',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
