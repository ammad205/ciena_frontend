# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfvo_app', '0003_auto_20141127_1255'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='users_tasks',
            new_name='task_params',
        ),
        migrations.RenameField(
            model_name='task_params',
            old_name='tasks',
            new_name='image',
        ),
    ]
