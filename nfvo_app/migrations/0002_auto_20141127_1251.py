# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfvo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users_tasks',
            name='username',
            field=models.TextField(max_length=100),
            preserve_default=True,
        ),
    ]
