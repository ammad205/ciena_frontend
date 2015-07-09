# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngn_grid', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datacenter',
            old_name='city',
            new_name='state',
        ),
    ]
