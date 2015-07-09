# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users_tasks',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('tasks', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
