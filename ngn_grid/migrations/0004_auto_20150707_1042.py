# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngn_grid', '0003_auto_20150707_1040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datacenter',
            old_name='ipaddr',
            new_name='ip',
        ),
    ]
